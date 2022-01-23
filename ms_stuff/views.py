import requests
from rest_framework.views import APIView, Response, status

from rest_framework_simplejwt.tokens import RefreshToken
from staff_stuff.models import Staff

from ms_stuff.graph_wrapper.config import constants

from role_stuff.permissions import IsADMOrReadOnly
from rest_framework.permissions import IsAuthenticated

from ms_stuff.graph_wrapper.mail import MailMS


# Create your views here.
class SignIn(APIView):
    def post(self, request):

        # request contains user's token obtained from client side
        token = request.data.get("token")

        if token is None:
            return Response({"error":"A token must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        
        # request made to MS api to know who the user is
        res = requests.get(
            constants["URL"]+"me",
            headers={"Authorization":"Bearer "+token, "Content-Type":"application/json"}
            )
        
        if res.status_code not in range(199,300):
            return Response({"MS_error":res.json()},status=status.HTTP_400_BAD_REQUEST)
        
        # get the user from local server's db
        id = res.json()["id"]
        user = Staff.objects.filter(ms_id=id).first()
        
        if user is None:
            return Response({"error":"No such SIMP user. This error shouldn't be possible actually."}, status=status.HTTP_404_NOT_FOUND)

        # generate access token for the user
        access = (RefreshToken.for_user(user).access_token)
        access["role"] = user.role
        access = str(access)
        return Response({"access":access},status=status.HTTP_200_OK)



class MailTo(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated, IsADMOrReadOnly]

    def post(self, request):
        required = {"subject", "text", "receiver"}

        if set(request.data).intersection(required) != required:
            x = required.difference(set(request.data).intersection(required)) 

            return Response({i:"this is a required field." for i in x}, status=status.HTTP_400_BAD_REQUEST)

        res = MailMS().send_from_request(request)
        if res.status_code not in range(199,300):
            return Response({"MS_error",res.json()},status=res.status_code)
        return Response({"message":"The mail is on its way :)"},status=status.HTTP_202_ACCEPTED)






