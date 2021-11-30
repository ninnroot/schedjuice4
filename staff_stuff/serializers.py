from django.db.models import fields
from rest_framework import serializers
from rest_framework.relations import ManyRelatedField
from .models import Department, Staff


# so that the StaffSerializer can use it.

class DepartmentOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = "__all__"
        

class StaffSerializer(serializers.ModelSerializer):
    department = DepartmentOnlySerializer(read_only=True)
        
    class Meta:
        model = Staff
        fields = "__all__"
        dept = 1
        

class StaffOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = "__all__"
        

class DepartmentSerializer(serializers.ModelSerializer):
    staff = StaffOnlySerializer(source="staff_set", many=True ,read_only=True)

    class Meta:
        model = Department
        fields = "__all__"
       


