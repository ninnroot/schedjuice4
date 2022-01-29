from rest_framework.views import APIView
from .helpers import getlist_helper, getdetails_helper, post_helper, put_helper, delete_helper
from .pagination import CustomPagination
from django.conf import settings

class GeneralList(APIView,CustomPagination):
    permission_classes = []
    related_fields = []
    read_only_fields = []
    excluded_fields = []
    if not settings.SET_PERMISSION:
        authentication_classes = []

    def get(self,request):
        return getlist_helper(self,request)

    def post(self, request):
        return post_helper(self,request)



class GeneralDetails(APIView,CustomPagination):
    permission_classes = []
    related_fields = []
    read_only_fields = []
    excluded_fields = []

    def get(self, request, obj_id):
        return getdetails_helper(self,request,obj_id)

    def put(self, request, obj_id):
        return put_helper(self,request, obj_id)

    def delete(self, request, obj_id):
        return delete_helper(self,request,obj_id)