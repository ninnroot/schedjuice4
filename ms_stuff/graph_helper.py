from email import message
import imp
import requests
import json

from rest_framework.serializers import ValidationError
from django.utils import timezone

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jinja2_stuff.core import env
import base64

from .auth import get_msal_app
from .config import settings



URL = "https://graph.microsoft.com/v1.0/"
BETA_URL = "https://graph.microsoft.com/beta/"

LICENSES = {
    "staff":"94763226-9b3c-4e75-a931-5c89701abe66",
    "student":"314c4481-f395-4525-be8b-2ec4bb1e9d91"
}

MAIL_GROUPS = {
    "allstaff":"5027018e-717d-4726-95ec-8d5b8ab51d1f",
    "allstudents":"3b6a0875-5a4c-4a0a-8a75-8c150c57b8b3"
}

def get_user(token, name="", me=False):
    if me:
        endpoint = URL+"me"
    else:
        endpoint = URL+"users/"+name
    user = requests.get(
        endpoint,
        headers={
            "Authorization":"Bearer "+token,
            
            }
    )
    return user.json()



class MSRequest:
    """
    The base class for preparing requests to be made to the MS graph API.
    Subclasses tailored for Users and Groups will be inherited from this class.
    Basically, I am building my own wrapper.
    """

    def __init__(self, token):
        self.token = token

    def build_header(self):
        return {
            "Authorization":"Bearer "+self.token,
            "Content-Type":"application/json"
        }

    def get_list(self, endpoint:str):
        return requests.get(URL+endpoint, headers=self.build_header())



class UserMS(MSRequest):
    """
    The class for making requests to /users endpoint of the graph API.
    """

    def get_licenses(self):
        return requests.get(URL+"subscribedSkus", headers=self.build_header())

    def getlist(self):
        return super().get_list("users")

    def get(self, user:str):
        return (requests.get(URL+"users/"+user, headers=self.build_header()))
    
    def post(self, request):
        dic = request.POST
        data = {
            "displayName":dic.get("dname"),
            "userPrincipalName":dic.get("email"),
            "passwordProfile":{
                "password":dic.get("password")
            },
            "accountEnabled":True,
            "mailNickname":"nickname",
            
        }
        return requests.post(URL+"users",data=json.dumps(data),headers=self.build_header())

    def patch(self, request, user:str):
        dic = request.POST
        data = {
            "mail":dic.get("email"),
            "usageLocation":"SG"
        }

        return requests.patch(URL+"users/"+ user, data=json.dumps(data), headers=self.build_header())

    def delete(self, user:str):
        return requests.delete(URL+"users/"+user, headers=self.build_header())

    def assign_license(self, user:str, license_type:str):
        return requests.post(
            URL+"users/"+user+"/assignLicense",
            json.dumps({
                "addLicenses":[{"skuId":LICENSES[license_type]}],
                "removeLicenses":[]
                }),
            headers=self.build_header())


class GroupMS(MSRequest):
    """
    The class for making requests to the graph API for creating groups and teams.
    """
    
    member_settings = {
        "allowCreateUpdateChannels":False,
        "allowDeleteChannels":False,
        "allowAddRemoveApps":False,
        "allowCreateUpdateRemoveTabs":False,
        "allowCreateUpdateRemoveConnectors":False
    }

    def __init__(self, token, group_type="educationClass"):

        # see available types of groups here:
        # https://docs.microsoft.com/en-us/MicrosoftTeams/get-started-with-teams-templates
        self.group_type = group_type
        
        super().__init__(token)

    def make_channel(self, name, fav=True):

        return {
            "displayName":name,
            "isFavouriteByDefault":fav
        }

    def getlist(self):
        return super().get_list("groups")

    def get(self, group:str):
        return (requests.get(URL+"groups/"+group, headers=self.build_header()))

    def post(self, request, visibility="Private"):

        dic = request.POST
        name = dic.get("name")
        if name is None:
            raise ValidationError("Class' name must not be null.")

        data = {
            "template@odata.bind":f"https://graph.microsoft.com/v1.0/teamsTemplates('{self.group_type}')",
            "displayName":name,
            "description":f"Hello, welcome to {name}. Created by Schedjuice4 at {timezone.now()}",
            "channels":[
                self.make_channel("Announcements"),
                self.make_channel("General")
            ],
            "mailEnabled":False,
            "memberSettings":self.member_settings,
            "owners@odata.bind":[
                "https://graph.microsoft.com/v1.0/users/fc4d758f-66fd-4167-902e-93da595ff0a3"
            ]
        }

        return requests.post(BETA_URL+"teams",data=json.dumps(data), headers=self.build_header())


    def delete(self, group:str):
        return requests.delete(URL+"groups/"+group, headers=self.build_header())


class MailMS(MSRequest):

    def __init__(self):
        x = get_msal_app(daemon=True)
        res = x.acquire_token_silent(settings["scopes"],account=None)
        if not res:
            res = x.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

        self.token = res["access_token"]
        super().__init__(self.token)

    def build_header(self):
        return {
            "Authorization":"Bearer "+self.token,
            "Content-Type":"text/plain"
        }


    def make_template(self, template:str, context):
        t = env.get_template(template)
        
        return t.render(context=context)


    def send_welcome(self, sender:str, receiver:str, context, subj="Welcome to Teacher Su center"):
        
        message = MIMEMultipart("alternative")
        message["subject"] = subj
        message["From"] = sender
        message["To"] = receiver
        
        body = MIMEText(self.make_template("welcome.html",context), "html")

        message.attach(body)

        message = base64.encodebytes(message.as_bytes())

        return requests.post(
            f"{URL}users/{sender}/sendMail",
            message,
            headers=self.build_header()
            )




        





