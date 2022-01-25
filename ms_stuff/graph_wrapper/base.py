import msal
import requests
import json

from ms_stuff.config import settings
from .config import constants

URL = constants["URL"]
BETA_URL = constants["BETA_URL"]
LICENSES = constants["LICENSES"]
SECURITY_GROUPS = constants["SECURITY_GROUPS"]


def get_msal_app(cache=None):
    
    
    app = msal.ConfidentialClientApplication(
        settings["app_id"],
        authority=settings["authority"],
        
        client_credential={
            "thumbprint": settings["thumbprint"],
            "private_key": open(settings['private_key_file']).read()
            },

    )
    return app



class MSRequest:
    """
    The base class for preparing requests to be made to the MS graph API.
    Subclasses tailored for Users and Groups will be inherited from this class.
    Basically, I am building my own wrapper.
    """

    day_mapper = {
        0:"Monday",
        1:"Tuesday",
        2:"Wednesday",
        3:"Thursday",
        4:"Friday",
        5:"Saturday",
        6:"Sunday"
    }


    @staticmethod
    def get_token():
        x = get_msal_app()
        res = x.acquire_token_silent(settings["scopes"], account=None)
        if not res:
            res = x.acquire_token_for_client(
                scopes=["https://graph.microsoft.com/.default"])

        MSRequest.token = res["access_token"]
        MSRequest.headers = {
            "Authorization": "Bearer " + MSRequest.token,
            "Content-Type": "application/json"
        }

    def __init__(self):
        self.get_token()

    def get(self, url, beta=False):
        x = URL
        if beta:
            x = BETA_URL
        return requests.get(x+url, headers=self.headers)

    def get_list(self, url: str, beta=False):
        x = URL
        if beta:
            x = BETA_URL
        return requests.get(x+url, headers=self.headers)

    @classmethod
    def post(cls, url, data, beta=False, encode=True):
        x = URL
        if beta:
            x = BETA_URL

        if encode:
            data=json.dumps(data)
        return requests.post(x+url, data, headers=cls.headers)

    def patch(self, url, data, beta=False):
        x = URL
        if beta:
            x = BETA_URL
        return requests.patch(x+url, json.dumps(data), headers=self.headers)

    def delete(self, url, beta=False):
        x = URL
        if beta:
            x = BETA_URL
        return requests.delete(x+url, headers=self.headers)

    def get_licenses(self):
        return self.get("subscribedSkus")
