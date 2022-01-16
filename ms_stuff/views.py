from http.client import ImproperConnectionState
from os import stat
from urllib import request
from django.http import HttpResponseRedirect
from rest_framework.views import APIView, Response, status
import msal
from staff_stuff.models import Staff
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from dateutil import tz, parser
from .auth import (
    get_sign_in_flow, get_token_from_code,
    store_user, remove_user_and_token, get_token
    )
from .graph_helper import get_user


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
            user = get_user(result["access_token"])
            store_user(request, user)
            staff = Staff.objects.get(email=user["userPrincipalName"])
            if staff:
                access = RefreshToken.for_user(staff).access_token
                return Response({"access":str(access)}, status=status.HTTP_200_OK)
            
            return Response({"message":"No such Microsoft account."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            
        
            return Response(result)


class SignOut(APIView):
    def get():
        remove_user_and_token(request)
        return Response({"message":"ok"})
