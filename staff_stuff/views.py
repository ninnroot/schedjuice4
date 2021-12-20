from rest_framework.views import APIView
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated
from .models import Department, Staff, Tag, StaffTag, StaffDepartment
from .serializers import (
                        DepartmentSerializer, StaffSerializer,
                        StaffTagSerializer, TagSerializer,
                        StaffDepartmentSerializer)
from .helpers import delete_helper, getlist_helper, getdetails_helper, post_helper, put_helper

# Create your views here.


class GeneralList(APIView,CustomPagination):
    permission_classes = []
    def get(self,request):
        return getlist_helper(self,request)

    def post(self, request):
        return post_helper(self,request)

class GeneralDetails(APIView,CustomPagination):
    permission_classes = []
    def get(self, request, obj_id):
        return getdetails_helper(self,request,obj_id)

    def put(self, request, obj_id):
        return put_helper(self,request, obj_id)

    def delete(self, request, obj_id):
        return delete_helper(self,request,obj_id)




class StaffList(GeneralList):
    model = Staff
    serializer = StaffSerializer
    related_fields = [
        "staffwork_set","staffsession_set",
        "stafftag_set","staffdepartment_set",
        "user_permissions","groups"
    ]    

class StaffDetails(GeneralList):
    model = Staff
    serializer = StaffSerializer



class DepartmentList(GeneralList):
    model = Department
    serializer = DepartmentSerializer
    related_fields = [
        "staffdepartment_set"
    ]


class DepartmentDetails(GeneralDetails):
    model = Department
    serializers = DepartmentSerializer



class TagList(GeneralList):
    model = Tag
    serializer = TagSerializer
    related_fields = ["stafftag_set"]
    
class TagDetails(GeneralDetails):
    model = Tag
    serializer = TagSerializer
    


class StaffTagList(GeneralList):
    model = StaffTag
    serializer = StaffTagSerializer

class StaffTagDetails(GeneralDetails):
    model = StaffTag
    serializer = StaffTagSerializer



class StaffDepartmentList(GeneralList):
    model = StaffDepartment
    serializer = StaffDepartmentSerializer

class StaffDepartmentDetails(GeneralDetails):
    model = StaffDepartment
    serializer = StaffDepartmentSerializer
