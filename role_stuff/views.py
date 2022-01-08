from schedjuice4.generic_views import GeneralDetails, GeneralList
from .models import Role
from .serializers import RoleSerializer

# Create your views here.


class RoleList(GeneralList):
    
    model = Role
    serializer = RoleSerializer

class RoleDetails(GeneralDetails):

    model = Role
    serializer = RoleSerializer

