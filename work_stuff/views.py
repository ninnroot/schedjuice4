from staff_stuff.views import GeneralList, GeneralDetails
from .models import Work, StaffWork, Session, StaffSession
from .serializers import SessionSerializer,StaffSessionSerializer, WorkSerializer, StaffWorkSerializer

# Create your views here.
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

