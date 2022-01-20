from rest_framework import serializers

from ms_stuff.auth import get_token
from ms_stuff.graph_helper import UserMS
from ms_stuff.graph_helper import MAIL_GROUPS
from ms_stuff.graph_helper import MailMS


def create_MS_user(request, data, mail=True):
    usr = UserMS(get_token(request))
        
    # create MS User
    res = usr.post(request)
    if res.status_code not in range(199,300):
        raise(serializers.ValidationError({"MS_error":res.json(),"step":1}))

    data["ms_id"] = res.json()["id"]
    
    
    # Update MS user for its mail and usage location
    res = usr.patch(request,request.POST.get("email"))
    if res.status_code not in range(199,300):
        raise(serializers.ValidationError({"MS_error":res.json(), "step":2}))

    # assign license and email address
    res = usr.assign_license(request.POST.get("email"),"staff")
    if res.status_code not in range(199,300):
        raise(serializers.ValidationError({"MS_error":res.json(), "step":3}))


    if mail:
        context = {
            "name":data["dname"],
            "email":data["email"],
            "password":data["password"]
        }
        x = MailMS().send_welcome(
            "staffy@teachersucenter.com",
            data["email"],
            context,
        )

        if x.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":x.json(), "step":"mail"})
        
