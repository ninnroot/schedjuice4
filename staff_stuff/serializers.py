
from rest_framework import serializers

from work_stuff.serializers import StaffSessionSerializerSession

from .models import Department, Staff, Tag, StaffTag, StaffDepartment
from work_stuff.serializers import StaffWorkSerializerWork, DynamicFieldsModelSerializer



# Only-serializers

class DepartmentOnlySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Department
        fields = "__all__"

class StaffOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = "__all__"

class TagOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"




class StaffTagOnlySerializer(serializers.ModelSerializer):    

    def validate(self, data):
        s = data["staff"]
        t = data["tag"]
        pos = data["pos"]
        obj = StaffTag.objects.filter(staff=s,tag=t).first()
        if obj is not None:
            raise serializers.ValidationError("Instance already exists.")

        obj = StaffTag.objects.filter(staff=s,pos=pos).first()
        if obj is not None:
            raise serializers.ValidationError({"pos":"The index is already taken."})
        return data

    class Meta:
        model = StaffTag
        fields = "__all__"
        dept=1

class StaffDepartmentOnlySerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        s = data["staff"]
        d = data["department"]
        pos = data["pos"]
        obj = StaffDepartment.objects.filter(staff=s,department=d).first()
        if obj is not None:
            raise serializers.ValidationError("Instance already exist.")

        obj = StaffDepartment.objects.filter(staff=s,pos=pos).first()
        if obj is not None:
            raise serializers.ValidationError({"pos":"The index is already taken."})

        if "is_primary" in data:
            ip = data["is_primary"]
            if ip == True:
                obj = StaffDepartment.objects.filter(staff=s, is_primary=True).first()
                if obj is not None:
                    raise serializers.ValidationError({"is_primary":"There can only be one primary department."})
        return data

    class Meta:
        model = StaffDepartment
        fields = "__all__"
        dept=1

class StaffDepartmentSerializer(DynamicFieldsModelSerializer):
    staff = StaffOnlySerializer(read_only=True)
    department = DepartmentOnlySerializer(read_only=True)

    class Meta:
        model = StaffDepartment
        fields = "__all__"
        dept=1

class StaffTagSerializer(DynamicFieldsModelSerializer):    
    staff = StaffOnlySerializer(read_only=True)
    tag = TagOnlySerializer(read_only=True)

    class Meta:
        model = StaffTag
        fields = "__all__"
        dept=1


class StaffTagSerializerTag(serializers.ModelSerializer):    
    tag = TagOnlySerializer(read_only=True)
    class Meta:
        model = StaffTag
        fields = "__all__"
        dept=1

class StaffTagSerializerStaff(serializers.ModelSerializer):    
    staff = StaffOnlySerializer(read_only=True)
    class Meta:
        model = StaffTag
        fields = "__all__"
        dept=1

class StaffDepartmentSerializerStaff(serializers.ModelSerializer):
    staff = StaffOnlySerializer(read_only=True)

    class Meta:
        model = StaffDepartment
        fields = "__all__"
        dept=1

class StaffDepartmentSerializerDept(serializers.ModelSerializer):
    departments = DepartmentOnlySerializer(read_only=True)

    class Meta:
        model = StaffDepartment
        fields = "__all__"
        dept=1

class StaffSerializer(DynamicFieldsModelSerializer):
    staffdepartments = StaffDepartmentSerializerDept(source="staffdepartment_set", many=True,read_only=True)
    stafftags = StaffTagSerializerTag(source="stafftag_set", many=True,read_only=True)
    staffworks = StaffWorkSerializerWork(source="staffwork_set", many=True, read_only=True)
    staffsessions = StaffSessionSerializerSession(source="staffsession_set", many=True, read_only=True)
    
    class Meta:
        model = Staff
        fields= "__all__"
        dept = 1

class DepartmentSerializer(DynamicFieldsModelSerializer):
    staffdepartments = StaffDepartmentSerializerStaff(source="staffdepartment_set",many=True,read_only=True)
    class Meta:
        model = Department
        fields = "__all__"
       
class TagSerializer(DynamicFieldsModelSerializer):
    stafftags = StaffTagSerializerStaff(source="stafftag_set",many=True, read_only=True)

    class Meta:
        model = Tag
        fields = "__all__"
        dept=1

