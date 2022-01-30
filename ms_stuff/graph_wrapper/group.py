import requests
import json

from .base import MSRequest

from django.core.exceptions import ValidationError
from .config import constants
from django.utils import timezone


class GroupMS(MSRequest):
    """
    The class for making requests to the graph API for creating groups and teams.
    """

    member_settings = {
        "allowCreateUpdateChannels": False,
        "allowDeleteChannels": False,
        "allowAddRemoveApps": False,
        "allowCreateUpdateRemoveTabs": False,
        "allowCreateUpdateRemoveConnectors": False
    }

    def __init__(self, group_id: str):
        self.group = group_id
        super().__init__()

    @staticmethod
    def make_channel(name, fav=True):

        return {
            "displayName": name,
            "isFavouriteByDefault": fav
        }

    @classmethod
    def create_group(cls, data=None, group_type="educationClass", name=None):

        cls.get_token()
        # see available types of groups here:
        # https://docs.microsoft.com/en-us/MicrosoftTeams/get-started-with-teams-templates

        if data:
            name = data.get("name")
        name = name

        if name is None:
            raise ValidationError(
                "A Request object must be provided else name kwarg must be specified. Both can't be none.")

        post_data = {
            "template@odata.bind": f"https://graph.microsoft.com/v1.0/teamsTemplates('{group_type}')",
            "displayName": name,
            "description": f"Hello, welcome to {name}. Created by Schedjuice4 at {timezone.now()}",
            "channels": [
                
                GroupMS.make_channel("General")
            ],
            "mailEnabled": False,
            "memberSettings": cls.member_settings,
            "owners@odata.bind": [
                "https://graph.microsoft.com/v1.0/users/"+constants["STAFFY_ID"]
            ],
            
            }

        return requests.post(constants["BETA_URL"]+"teams", json.dumps(post_data), headers=cls.headers)

    def get(self):
        return super().get("groups/"+self.group)

    @classmethod
    def get_list(cls):
        cls.get_token()
        return super().get_list("groups")

    def create_channel(self,display_name:str):
        c = self.make_channel(display_name)

        return self.post(f"teams/{self.group}/channels",c)

    def remove_member(self, member:str, user_type:str):
        return  super().delete(f"groups/{self.group}/{user_type}/{member}/$ref")

    def delete(self):
        return super().delete("groups/"+self.group)

    
        