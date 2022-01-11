from os import path
import re
from django.core.exceptions import NON_FIELD_ERRORS
from rest_framework.exceptions import bad_request
from rest_framework.permissions import BasePermission
from staff_stuff.models import Staff
from work_stuff.models import StaffWork, StaffSession

def get_role_helper(request):
    user = request.user
    if user:
        user = Staff.objects.get(pk=user.id)
        if user.role is not None:
            role = user.role.shorthand
            return role
    return None


def readonly_determiner(self, request, view, role):
    rf = set(view.model.read_only_fields[role]).intersection(set(request.data.keys()))
    if len(rf)!=0:
        self.message = f"You do not have permission to update these fields: {rf}"
        if "status" in rf:
            self.message = "You think you are so clever, huh?"
        return False
    return True


def owner_determiner(model, user,obj):
    dic = {
        "Staff":user.id==obj.id,
        "Work":StaffWork.objects.filter(work=obj.id,staff=user.id).exists(),
        "Session":StaffSession.objects.filter(session=obj.id,staff=user.id).exists()
    }
    try:
        x =dic[model]
        return x
    except KeyError:
        return False


class StatusCheck(BasePermission):
    message = "Status check failed."

    def has_permission(self, request, view):
        
        user = Staff.objects.get(pk=request.user.id)

        if view.model.__name__ == "Staff":
            if user.status == "active" or user.status == "on leave":
                return True
            if user.status == "unapproved":
                self.message = "Please wait for your account's approval. We will notify via email once your account is activated."
                return False
            elif user.status == "retired":
                self.message = "Your account has been retired. If this might be an accident, please contact the admins."
                return False
            else:
                self.message = "Please finish your account registration"
                return False

        return False


class IsSDMOrReadOnly(BasePermission):
    message = "You do not have permission to perform this action. SDM  role is required."
    
    def has_permission(self, request, view):        
        user = Staff.objects.get(pk=request.user.id)

        if user.role is not None:
            if user.role.shorthand == "SDM" or request.method == "GET":                    
                return True
        
        return False

    def has_object_permission(self, request, view, obj):
        return True

class IsADMOrReadOnly(BasePermission):
    message = "You do not have permission to perform this action. At least the ADM role is required."

    def has_permission(self, request, view):
        role = get_role_helper(request)
        if role:
            if request.method == "GET":
                return True
            elif role == "SDM" or role == "ADM" :
                return readonly_determiner(self, request, view, role)
                
        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsOwnerOrReadOnly(BasePermission):
    message = "You do not have permission to perform this action. You are not the owner."

    def has_permission(self, request, view):
        role = get_role_helper(request)
        if role:
            if request.method == "GET":
                return True
            elif role == "SDM":
                return True
            elif role == "ADM":
                return readonly_determiner(self, request, view, role)
            elif role == "USR":
                return True

        return False

    def has_object_permission(self, request, view, obj):
        role = get_role_helper(request)

        if request.method == "GET":
            return True
        elif role == "SDM":
            return True
        elif role == "ADM":
            return readonly_determiner(self, request, view, role)
        elif role == "USR":
            
            x = owner_determiner(view.model.__name__,Staff.objects.get(pk=request.user.id),obj)
            if x:
                return readonly_determiner(self, request, view, role)
        return False

class RegistrationPhase(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        banned_lst = [
            "status",
            "role",
        ]

        for i in banned_lst:
            if i in request.data.keys():
                
                self.message = "What the fuck are you doing?! >:( . If you want to create a superuser, do it via the Python shell."
                return False
        return True

    def has_object_permission(self, request, view, obj):
        return True

