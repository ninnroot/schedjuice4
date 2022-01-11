from rest_framework import request
from schedjuice4.generic_views import GeneralDetails, GeneralList
from rest_framework.permissions import IsAuthenticated

from role_stuff.permissions import IsADMOrReadOnly, IsOwnerOrReadOnly
from .models import Department, Staff, Tag, StaffTag, StaffDepartment
from .serializers import (
                        DepartmentSerializer, StaffSerializer,
                        StaffTagSerializer, TagSerializer,
                        StaffDepartmentSerializer)

from role_stuff.permissions import RegistrationPhase

# Create your views here.


class StaffList(GeneralList):
    authentication_classes = []
    model = Staff
    serializer = StaffSerializer
    related_fields = [
        "staffwork_set","staffsession_set",
        "stafftag_set","staffdepartment_set",
        "user_permissions","groups", "role"
    ]
    
    permission_classes = [RegistrationPhase]
    

class StaffDetails(GeneralDetails):
    model = Staff
    serializer = StaffSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class DepartmentList(GeneralList):
    model = Department
    serializer = DepartmentSerializer
    related_fields = [
        "staffdepartment_set"
    ]
    


class DepartmentDetails(GeneralDetails):
    model = Department
    serializer = DepartmentSerializer



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
