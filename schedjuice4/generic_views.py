from rest_framework.views import APIView
from .helpers import getlist_helper, getdetails_helper, post_helper, put_helper, delete_helper, search_helper
from .pagination import CustomPagination
from django.conf import settings

class GeneralList(APIView,CustomPagination):
    permission_classes = []
    related_fields = []


    if not settings.SET_PERMISSION:
        authentication_classes = []

    def get(self,request, **kwargs):
        return getlist_helper(self,request)

    def post(self, request, **kwargs):
        return post_helper(self,request)

    def search(self, request, **kwargs):
        return search_helper(self,request)



class GeneralDetails(APIView,CustomPagination):
    permission_classes = []
    related_fields = []


    def get(self, request, obj_id, **kwargs):
        return getdetails_helper(self,request,obj_id)

    def put(self, request, obj_id, **kwargs):
        return put_helper(self,request, obj_id)

    def delete(self, request, obj_id, **kwargs):
        return delete_helper(self,request,obj_id)