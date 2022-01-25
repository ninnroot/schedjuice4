from rest_framework.exceptions import APIException


class MSException(APIException):
    status_code = 404
    default_detail = "No such Microsoft account."
    default_code = "no_ms_account"


class WrapperException(Exception):
    pass
