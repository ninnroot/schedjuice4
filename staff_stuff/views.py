from rest_framework import request
from rest_framework import permissions
from schedjuice4.generic_views import GeneralDetails, GeneralList
from rest_framework.permissions import IsAuthenticated
from .models import Department, Staff, Tag, StaffTag, StaffDepartment
from .serializers import (
                        DepartmentSerializer, StaffSerializer,
                        StaffTagSerializer, TagSerializer,
                        StaffDepartmentSerializer)

from role_stuff.permissions import RegistrationPhase,IsADMOrReadOnly, IsOwnerOrReadOnly, StatusCheck

# Create your views here.


class StaffList(GeneralList):
    
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
    permission_classes = [IsAuthenticated, StatusCheck,IsOwnerOrReadOnly]


class DepartmentList(GeneralList):
    model = Department
    serializer = DepartmentSerializer
    related_fields = [
        "staffdepartment_set"
    ]
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]
    


class DepartmentDetails(GeneralDetails):
    model = Department
    serializer = DepartmentSerializer
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]



class TagList(GeneralList):
    model = Tag
    serializer = TagSerializer
    related_fields = ["stafftag_set"]
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]

class TagDetails(GeneralDetails):
    model = Tag
    serializer = TagSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsADMOrReadOnly]
    


class StaffTagList(GeneralList):
    model = StaffTag
    serializer = StaffTagSerializer
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]

class StaffTagDetails(GeneralDetails):
    model = StaffTag
    serializer = StaffTagSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsADMOrReadOnly]



class StaffDepartmentList(GeneralList):
    model = StaffDepartment
    serializer = StaffDepartmentSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsADMOrReadOnly]

class StaffDepartmentDetails(GeneralDetails):
    model = StaffDepartment
    serializer = StaffDepartmentSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsADMOrReadOnly]
