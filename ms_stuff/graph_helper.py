from cgitb import reset
from email import header
import imp
import requests
import json

URL = "https://graph.microsoft.com/v1.0/"

LICENSES = {
    "staff":"94763226-9b3c-4e75-a931-5c89701abe66",
    "student":"314c4481-f395-4525-be8b-2ec4bb1e9d91"
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
    def __init__(self, token):
        self.token = token

    def build_header(self):
        return {
            "Authorization":"Bearer "+self.token,
            "Content-Type":"application/json"
        }



class UserMS(MSRequest):
    def __init__(self, token:str):
        super().__init__(token)

    def get_licenses(self):
        return requests.get(URL+"subscribedSkus", headers=self.build_header())

    def getlist(self):
        return (requests.get(URL+"users", headers=self.build_header()))
        

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

    def patch(self, request, user):
        dic = request.POST
        data = {
            "mail":dic.get("email"),
            "usageLocation":"SG"
        }
        return requests.patch(URL+"users/"+ user, data=json.dumps(data), headers=self.build_header())

    def assign_license(self, user:str, license_type:str):
        return requests.post(
            URL+"users/"+user+"/assignLicense",
            json.dumps({
                "addLicenses":[{"skuId":LICENSES[license_type]}],
                "removeLicenses":[]
                }),
            headers=self.build_header())
