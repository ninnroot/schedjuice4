from rest_framework import serializers
from staff_stuff.views import GeneralList, GeneralDetails
from .models import Work, StaffWork, Session, StaffSession, Category
from .serializers import SessionSerializer,StaffSessionSerializer, WorkSerializer, StaffWorkSerializer, CategorySerializer

# Create your views here.
class CategoryList(GeneralList):
    model = Category
    serializer = CategorySerializer
    related_fields = ["work_set"]

class CategoryDetails(GeneralDetails):
    model = Category
    serializer = CategorySerializer
    related_fields = ["work_set"]



class WorkList(GeneralList):
    model = Work
    serializer = WorkSerializer

class WorkDetails(GeneralDetails):
    model = Work
    serializer = WorkSerializer



class SessionList(GeneralList):
    model = Session
    serializer = SessionSerializer

class SessionDetails(GeneralDetails):
    model = Session
    serializer = SessionSerializer



class StaffSessionList(GeneralList):
    model = StaffSession
    serializer = StaffSessionSerializer

class StaffSessionDetails(GeneralDetails):
    model = StaffSession
    serializers = StaffSessionSerializer



class StaffWorkList(GeneralList):
    model = StaffWork
    serializer = StaffWorkSerializer

class StaffWorkDetails(GeneralDetails):
    model = StaffWork
    serializer = StaffWorkSerializer



