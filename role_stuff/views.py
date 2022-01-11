from rest_framework.permissions import IsAuthenticated
from schedjuice4.generic_views import GeneralDetails, GeneralList
from .models import Role
from .serializers import RoleSerializer
from .permissions import IsSDMOrReadOnly
# Create your views here.


class RoleList(GeneralList):

    model = Role
    serializer = RoleSerializer
    permission_classes = [IsAuthenticated, IsSDMOrReadOnly]

class RoleDetails(GeneralDetails):

    permission_classes = [IsAuthenticated, IsSDMOrReadOnly]
    model = Role
    serializer = RoleSerializer

