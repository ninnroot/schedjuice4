from .user import UserMS
from .mail import MailMS

from .config import constants

from rest_framework.serializers import ValidationError


def raise_error(request,step:str):
    if request.status_code not in range(199,300):
        raise ValidationError({"MS_error":request.json(),"step":step})
    
    return request

def start_user_creation_flow(request, data, user_type:str, mail=True, pw=None):
    user = UserMS(request.POST.get("email"))

    if pw is None:
        pw = constants["DEFAULT_PASSWORD"]

    # create MS user
    res = raise_error(user.create_with_req(request,pw),"create")
    
    data["ms_id"] = res.json()["id"]


    # update email addresss and usage location with a separate patch request
    res = raise_error(user.patch_with_req(request), "update")


    # assign license
    res = raise_error(user.assign_license(user_type),"license")


    # send welcome email (optional step)
    if mail:
        context = {"name": data["dname"], "email":data["email"], "password":pw}
        res = MailMS().send_welcome("staffy@teachersucenter.com",data["email"],context)
        res = raise_error(res)


    if user_type == "staff":
        # add to security group
        user.add_to_group(data["ms_id"],constants["SECURITY_GROUP"]["allstaff"],"members")


