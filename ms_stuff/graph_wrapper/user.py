from .base import MSRequest

from .config import constants



class UserMS(MSRequest):
    """
    The class for making requests to /users endpoint of the graph API.
    """

    def __init__(self, user: str):
        self.user = user
        super().__init__()

    def get(self):
        return super.get("users/"+self.user)

    def get_list(self):
        return super().get_list("users", headers=self.build_header())

    def create_with_req(self, request, password=None):
        dic = request.data
        pw = dic.get("password")
        if password:
            pw = password

        data = {
            "displayName": dic.get("dname"),
            "userPrincipalName": dic.get("email"),
            "passwordProfile": {
                "password": pw
            },
            "accountEnabled": True,
            "mailNickname": "nickname",

        }
        return self.post("users", data)

    def patch_with_req(self, request):
        dic = request.data
        data = {
            "mail": dic.get("email"),
            "usageLocation": "SG"
        }

        return self.patch("users/" + self.user, data)

    def delete(self):
        return super().delete("users/"+self.user)

    def add_to_group(self, user_id: str, group: str, role: str):

        data = {}

        if role == "owners":
            data = {"@odata.id": "https://graph.microsoft.com/v1.0/users/"+user_id}

        elif role == "members":
            data = {
                "@odata.id": "https://graph.microsoft.com/v1.0/directoryObjects/"+user_id}

        url = f"groups/{group}/{role}/$ref"

        return self.post(url, data)

    def assign_license(self, license_type: str):
        return self.post(
            "users/"+self.user+"/assignLicense", {
                "addLicenses": [{"skuId": constants["LICENSES"][license_type]}],
                "removeLicenses": []
            })
