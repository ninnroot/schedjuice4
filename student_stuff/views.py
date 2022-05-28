from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from rest_framework.views import APIView, status, Response

from schedjuice4.generic_views import GeneralDetails, GeneralList
from .models import Student, StudentWork
from .serializers import StudentSerializer, StudentWorkSerializer

from role_stuff.permissions import IsADMOrReadOnly, StatusCheck
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class StudentList(GeneralList):
    model = Student
    serializer = StudentSerializer
    related_fields = [
        "studentwork_set__work"
    ]

    permission_classes = [IsAuthenticated, StatusCheck, IsADMOrReadOnly]



class StudentDetails(GeneralDetails):
    model = Student
    serializer = StudentSerializer
    permission_classes = [IsAuthenticated, StatusCheck, IsADMOrReadOnly]



class StudentWorkList(GeneralList):
    model = StudentWork
    serializer = StudentWorkSerializer
    related_fields = [
        "student",
        "work"
    ]
    permission_classes = [IsAuthenticated, StatusCheck, IsADMOrReadOnly]



class StudentWorkDetails(GeneralDetails):
    model = StudentWork
    serializer = StudentWorkSerializer
    permission_classes = [IsAuthenticated, StatusCheck, IsADMOrReadOnly]



class StudentSearch(GeneralList):
    related_fields = [
        "studentwork_set",
        "studentwork_set__student",
        "studentwork_set__work"

    ]
    permission_classes = [IsAuthenticated, StatusCheck, IsADMOrReadOnly]
    model = Student
    serializer = StudentSerializer


    def get(self, request, **kwargs):
        return super().search(request, **kwargs)



