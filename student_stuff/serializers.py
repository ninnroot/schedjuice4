from webbrowser import get
from rest_framework import serializers
from schedjuice4.serializers import DynamicFieldsModelSerializer, status_check
from work_stuff.serializers import WorkOnlySerializer

from .models import Student, StudentWork

from ms_stuff.graph_wrapper.user import UserMS
from ms_stuff.graph_wrapper.tasks import start_user_creation_flow



class StudentOnlySerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Student
        fields = "__all__"



class StudentWorkSerializer(DynamicFieldsModelSerializer):
    student_details = StudentOnlySerializer(source="student", fields="id,email,dname,ename,profile_pic,card_pic",read_only=True)
    work_details = WorkOnlySerializer(source="work",fields="id,name,status", read_only=True)


    def create(self, data):
        w = data.get("work")
        u = data.get("student")
        
        x = StudentWork.objects.filter(work=w,student=u).first()
        if x is not None:
            raise serializers.ValidationError("Instance already exists.")
        
        res = UserMS(u.email).add_to_group(u.ms_id, w.ms_id, "members")

        if res.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":res.json()})

        return super().create(data)

    class Meta:
        model = StudentWork
        fields = "__all__"



class StudentSerializer(DynamicFieldsModelSerializer):
    works = StudentWorkSerializer(source="studentwork_set",fields="id,student_details,work_details", many=True, read_only=True)

    _gender_lst = ["male","female","non-binary","other"]

    def validate(self, attrs):
        if attrs.get("gender"):
            if attrs.get("gender") not in self._gender_lst:
                raise serializers.ValidationError({"gender":"Gender must be in "+ self._gender_lst})
        return super().validate(attrs)

    def create(self, data):
        if not self.context.get("silent"):
            print(data)
            start_user_creation_flow(self.context.get('r'),data,"student")

        return super().create(data)

    class Meta:
        model = Student

        fields = "__all__"
        extra_kwargs = {
            "ms_id":{"required":False},
            "password":{"write_only":True}
        }


