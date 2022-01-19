
from django.http import HttpResponseRedirect
from rest_framework.views import APIView, Response, status
import msal
from staff_stuff.models import Staff
from rest_framework_simplejwt.tokens import RefreshToken
from dateutil import tz, parser
from .auth import (
    get_sign_in_flow, get_token_from_code,
    store_user, remove_user_and_token, get_token
    )
from .graph_helper import UserMS, get_user


def callback(request):
    result = get_token_from_code(request)
    return Response({"message":"ok"})


# Create your views here.
class SignIn(APIView):
    def get(self, request):
        flow = get_sign_in_flow()
        try:
            request.session["auth_flow"] = flow
        
        except Exception as e:
            print("Error",e)

        return Response(flow["auth_uri"])

class Redirected(APIView):
    def get(self, request):
        result = get_token_from_code(request)
        try:
            user = get_user(result["access_token"],me=True)
            store_user(request, user)
            staff = Staff.objects.filter(email=user["userPrincipalName"]).first()
            if staff:
                access = RefreshToken.for_user(staff).access_token
                return Response({"access":str(access)}, status=status.HTTP_200_OK)
            
            return Response({"message":"No such Microsoft account."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            
        
            return Response({"error":str(e)})


class SignOut(APIView):
    def get(self, request):
        remove_user_and_token(request)
        return Response({"message":"Successfully signed out."})


class Test(APIView):

    def get(self, request):
        res = UserMS(get_token(request)).get_licenses()
        return Response(res.json())

    def post(self, request):
        res = UserMS(get_token(request)).post(request)
        return Response(res)
