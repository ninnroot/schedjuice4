from .user import UserMS
from .mail import MailMS

from .config import constants
import time

from rest_framework.serializers import ValidationError


def raise_error(request,step:str):
    if request.status_code not in range(199,300):
        raise ValidationError({"MS_error":request.json(),"step":step})
    
    return request

def start_user_creation_flow(request, data, user_type:str, mail=True):

    # This is a mess. I should have used concurrency. But, it'd further complicate
    # the code, so nevermind. Maybe in Schedjuice5 :)

    user = UserMS(request.data.get("email"))
    pw = data.get("password")
    # create MS user
    res = raise_error(user.create_with_req(request,pw),"create")
    
    data["ms_id"] = res.json()["id"]

    time.sleep(2.5)
    # update email addresss and usage location with a separate patch request
    res = user.patch_with_req(request)

    if res.status_code == 404:
        res = user.patch_with_req(request)

    if res.status_code not in range(199,300):
        raise ValidationError({"MS_error":res.json(),"step":"update"})
    
    time.sleep(1.5)
    # assign license
    res = user.assign_license(user_type)

    if res.status_code == 404:
        res = user.assign_license(user_type)

    if res.status_code not in range(199,300):
        raise ValidationError({"MS_error":res.json(),"step":"license"})


    # send welcome email (optional step)
    if mail:
        # context = {"name": data["dname"], "email":data["email"], "password":data["password"]}
        # res = MailMS().send_welcome("staffy@teachersucenter.com",data["email"],context)
        # res = raise_error(res, "mail sending")

        if "gmail" in data:
            context = {"name": data["dname"], "email":data["email"], "password":data["password"]}
            res = MailMS().send_welcome("staffy@teachersucenter.com",data["gmail"],context)
            res = raise_error(res, "gmail sending")


    if user_type == "staff":
        # add to security group
        res = user.add_to_group(data["ms_id"],constants["SECURITY_GROUPS"]["allstaff"],"members")
        if res.status_code not in range(199,300):
            raise ValidationError({"MS_error":res.json(),"step":"security group"})

        res = user.add_to_group(data["ms_id"],constants["GROUPS"]["ms_support"],"members")
        if res.status_code not in range(199,300):
            raise ValidationError({"MS_error":res.json(),"step":"ms-support group"})

