from django.db import models
from django.db.models.lookups import Transform
from rest_framework import serializers
from .models import Work, StaffWork, Session, StaffSession, Category
from staff_stuff.models import Staff



class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = (kwargs.pop('fields', None))
        
        if fields:
            fields = fields.split(",")
        
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            
            for field_name in existing - allowed:
                self.fields.pop(field_name)
             

class CategoryOnlySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"

class StaffOnlySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Staff
        fields = "__all__"

class WorkOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"

class SessionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"


class StaffSessionSerializer(DynamicFieldsModelSerializer):
    staff_details = StaffOnlySerializer(read_only=True)
    session_details = SessionSerializer(read_only=True)

    def validate(self, data):
        s = data["staff"]
        se = data["session"]
            
        
        obj = StaffWork.objects.filter(staff=s, work=se.work).first()
        if obj is None:
            raise serializers.ValidationError("Staff is not related to Session's Work.")
        return data
    class Meta:
        model = StaffSession
        fields = "__all__"


class StaffSessionSerializerSession(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)

    class Meta:
        model = StaffSession
        fields = "__all__"


class StaffWorkSerializer(DynamicFieldsModelSerializer):
    staff_details = StaffOnlySerializer(read_only=True)
    work_details = WorkOnlySerializer(read_only=True)

    def validate(self, data):
        s = data["staff"]
        w = data["work"]
        obj = StaffWork.objects.filter(staff=s,work=w).first()
        if obj is not None:
            raise serializers.ValidationError("Instance already exists.")
        return data
    class Meta:
        model = StaffWork
        fields = "__all__"

class StaffWorkSerializerStaff(serializers.ModelSerializer):
    staff = StaffOnlySerializer(read_only=True)

    class Meta:
        model = StaffWork
        fields = "__all__"

class StaffWorkSerializerWork(serializers.ModelSerializer):
    work = WorkOnlySerializer(read_only=True)
    class Meta:
        model = StaffWork
        fields = "__all__"

class CategorySerializer(DynamicFieldsModelSerializer):
    works = WorkOnlySerializer(read_only=True,many=True)

    class Meta:
        model = Category
        fields = "__all__"

class WorkSerializer(DynamicFieldsModelSerializer):
    staffworks = StaffWorkSerializerStaff(source="staffwork_set", many=True, read_only=True)
    sessions = SessionSerializer(source="session_set", many=True, read_only=True)
    category = CategoryOnlySerializer(read_only=True)

    class Meta:
        model = Work
        fields = "__all__"


