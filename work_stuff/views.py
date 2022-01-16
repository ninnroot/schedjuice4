from schedjuice4.generic_views import GeneralList, GeneralDetails
from .models import Work, StaffWork, Session, StaffSession, Category
from .serializers import SessionSerializer,StaffSessionSerializer, WorkSerializer, StaffWorkSerializer, CategorySerializer
from role_stuff.permissions import IsADMOrReadOnly, IsSDMOrReadOnly, IsOwnerOrReadOnly, StatusCheck
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CategoryList(GeneralList):
    model = Category
    serializer = CategorySerializer
    related_fields = ["work_set"]
    permission_classes = [IsAuthenticated,StatusCheck, IsSDMOrReadOnly]

class CategoryDetails(GeneralDetails):
    model = Category
    serializer = CategorySerializer
    permission_classes = [IsAuthenticated,StatusCheck, IsSDMOrReadOnly]



class WorkList(GeneralList):
    model = Work
    serializer = WorkSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsOwnerOrReadOnly]

class WorkDetails(GeneralDetails):
    model = Work
    serializer = WorkSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsOwnerOrReadOnly]



class SessionList(GeneralList):
    model = Session
    serializer = SessionSerializer
    permission_classes = [IsAuthenticated,StatusCheck, IsOwnerOrReadOnly]

class SessionDetails(GeneralDetails):
    model = Session
    serializer = SessionSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsOwnerOrReadOnly]



class StaffSessionList(GeneralList):
    model = StaffSession
    serializer = StaffSessionSerializer
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]

class StaffSessionDetails(GeneralDetails):
    model = StaffSession
    serializers = StaffSessionSerializer
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]



class StaffWorkList(GeneralList):
    model = StaffWork
    serializer = StaffWorkSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsADMOrReadOnly]

class StaffWorkDetails(GeneralDetails):
    model = StaffWork
    serializer = StaffWorkSerializer
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]



