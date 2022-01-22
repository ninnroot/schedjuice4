import requests
import json

from .base import MSRequest

from django.core.exceptions import ValidationError
from .config import constants



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
    def create_group(cls, request=None, group_type="educationClass", name=None):

        # see available types of groups here:
        # https://docs.microsoft.com/en-us/MicrosoftTeams/get-started-with-teams-templates

        if request:
            name = request.POST.get("name")
        name = name

        if name is None:
            raise ValidationError(
                "A Request object must be provided else name kwarg must be specified. Both can't be none.")

        data = {
            "template@odata.bind": f"https://graph.microsoft.com/v1.0/teamsTemplates('{group_type}')",
            "displayName": name,
            "description": f"Hello, welcome to {name}. Created by Schedjuice4 at {timezone.now()}",
            "channels": [
                GroupMS.make_channel("Announcements"),
                GroupMS.make_channel("General")
            ],
            "mailEnabled": False,
            "memberSettings": cls.member_settings,
            "owners@odata.bind": [
                "https://graph.microsoft.com/v1.0/users/"+constants["STAFFY_ID"]
            ]
        }

        return requests.post(constants["BETA_URL"]+"teams", json.dumps(data), headers=cls.headers)

    def get(self):
        return super().get("groups/"+self.group)

    def get_list(self):
        return super().get_list("groups")

    def delete(self):
        return super().delete("groups/"+self.group)