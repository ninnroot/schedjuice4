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
        "studentwork_set"
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



class StudentSearch(APIView):
    
    permission_classes = [IsAuthenticated, StatusCheck, IsADMOrReadOnly]

    def get(self, request, **kwargs):
        q = request.GET.get("q")
        if not q:
            return Response({"error":"The request must contain 'q' query param."}, status=status.HTTP_400_BAD_REQUEST)

        if q:

            students = Student.objects.all()
            x = students.annotate(
                    similarity=TrigramSimilarity("dname",q),
                ).filter(similarity__gt=0.35)
            
            y=students.annotate(
                similarity=TrigramSimilarity("email",q)
            ).filter(similarity__gt=0.35)
            search = (x|y).order_by("-similarity")

            res = StudentSerializer(data=search,many=True,fields="id,dname,email,ms_id")
            res.is_valid()

            res = {
                "count":search.count(),
                "data":res.data
            }

            return Response(res)



