from schedjuice4.serializers import DynamicFieldsModelSerializer, status_check
from rest_framework import serializers

from .models import Work, StaffWork, Session, StaffSession, Category
from staff_stuff.models import Staff
from role_stuff.serializers import RoleOnlySerializer
             
from ms_stuff.graph_wrapper.group import GroupMS
from ms_stuff.graph_wrapper.user import UserMS
from ms_stuff.graph_wrapper.outlook import EventMS



class CategoryOnlySerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"

class StaffOnlySerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Staff
        fields = "__all__"

class WorkOnlySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"


class SessionSerializer(DynamicFieldsModelSerializer):
    
    def create(self, data):

        x = Session.objects.create(**data)
        
        res = EventMS.create_event_for_session(x)
        if res.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":res.json})

        x.event_id = res["id"]
        x.save()
        return x

    class Meta:
        model = Session
        fields = "__all__"
        extra_kwargs = {
            "event_id":{"required":False}
        }


class StaffSessionSerializer(DynamicFieldsModelSerializer):
    staff_details = StaffOnlySerializer(source="staff", fields="id,email,dname,ename,uname,profile_pic,card_pic",read_only=True)
    session_details = SessionSerializer(source="session",fields="id,work,day,time_from,time_to", read_only=True)
    role_details = RoleOnlySerializer(source="role_set", fields="id,name,shorthand,is_specific", read_only=True)


    def validate(self, data):
        s = data.get("staff")
        se = data.get("session")
        
        obj = StaffSession.objects.filter(staff=s,session=se).exists()
        if not obj:
            raise serializers.ValidationError("Instance already exists.")
        
        obj = StaffWork.objects.filter(staff=s, work=se.work).exists()
        if not obj:
            raise serializers.ValidationError("Staff is not related to Session's Work.")
        return data


    def create(self, data):
        se = data.get("session")
        e = EventMS(se.event_id,se.work.organizer.email)
        res = e.add_attendee(data.get("staff"),StaffSession.objects.filter(session=se).all())

        if res.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":res.json()})
        
        
        return super().create(data)


    class Meta:
        model = StaffSession
        fields = "__all__"



class StaffWorkSerializer(DynamicFieldsModelSerializer):
    staff_details = StaffOnlySerializer(source="staff",fields="id,email,dname,ename,uname,profile_pic,card_pic", read_only=True)
    work_details = WorkOnlySerializer(source="work", fields="id,name", read_only=True)
    role_details = RoleOnlySerializer(source="role", fields="id,name,shorthand,is_specific", read_only=True)

    def validate(self, data):
        s = data.get("staff")
        w = data.get("work")
        obj = StaffWork.objects.filter(staff=s,work=w).first()
        if obj is not None:
            raise serializers.ValidationError("Instance already exists.")
        return super().validate(data)

    def create(self, data):
        w = data["work"]
        u = data["staff"]
        res = UserMS(u.email).add_to_group(u.ms_id,w.ms_id,"owners")
        
        if res.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":res.json()})

        return super().create(data,)

    class Meta:
        model = StaffWork
        fields = "__all__"



class CategorySerializer(DynamicFieldsModelSerializer):
    works = WorkOnlySerializer(read_only=True,many=True)

    class Meta:
        model = Category
        fields = "__all__"



class WorkSerializer(DynamicFieldsModelSerializer):
    staff = StaffWorkSerializer(source="staffwork_set",fields="id,staff_details,role_details" , many=True, read_only=True)
    sessions = SessionSerializer(source="session_set", many=True, read_only=True)
    category = CategoryOnlySerializer(read_only=True)
    _status_lst = [
        "pending",
        "ready",
        "active",
        "ended",
        "on halt"
    ]
    def validate(self, data):
        status = data.get("status")
        if not status_check(status, self._status_lst):
            raise serializers.ValidationError({"status":f"Status '{status}' not allowed. Allowed statuses are {self._status_lst}."})

        return super().validate(data) 

    
    def create(self, data):
        r = self.context.get("r")
        res = GroupMS.create_group(r)
        
        if res.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":res.json()})
        
        # get the group id from Graph API which is in the headers.
        # save that together with the crated Work.
        gp_id = res.headers["Content-Location"].split("'")[1::2][0]
        data["ms_id"] = gp_id


    def update(self, instance, data):
        
        # replacing the organizer
        if data.get("organizer"):
            x = data.get("organizer")
            if instance.organizer:
                res = GroupMS(instance.ms_id).remove_member(instance.organizer.ms_id,"owners")
                if res.status_code not in range(199,300):
                    return serializers.ValidationError({"MS_error":res.json(),"step":"removing old organizer"})

            res = UserMS(x).add_to_group(x.ms_id,instance.ms_id,"owners")
            if res.status_code not in range(199,300):
                return serializers.ValidationError({"MS_error":res.json(),"step":"adding organizer"})
            
            instance = super().update(instance,data)

            return instance


    class Meta:
        model = Work
        fields = "__all__"
        extra_kwargs = {
            "ms_id":{"required":False}
        }


