from work_stuff.models import Work
from django.db import models
from schedjuice4.models import CustomModel

from django.core.validators import RegexValidator

from datetime import date


# Create your models here.

class Student(CustomModel):

    email =  models.EmailField(unique=True)
    ms_id = models.CharField(max_length=256, unique=True)
    dname = models.CharField(max_length=128, default="Display Name")
    ename = models.CharField(max_length=128, default="Nickname")
    description = models.TextField(default="Description...")
    status = models.CharField(max_length=128, default="active")
    dob = models.DateField(default=date(2000,1,1))
    gender = models.CharField(max_length=32, default="")
    ph_num = models.CharField(max_length=16,default="", validators=[RegexValidator(r'^\d{1,11}$')])
    profile_pic = models.ImageField(default="stu_profile/default.jpg", upload_to="stu_profile")
    cover_pic = models.ImageField(default="stu_cover/default.jpg",upload_to="stu_cover")
    card_pic = models.ImageField(default="stu_card/default.jpg", upload_to="stu_card")

    house_num = models.CharField(max_length=16, default="")
    street = models.CharField(max_length=128, default="")
    township = models.CharField(max_length=128, default="")
    city = models.CharField(max_length=128, default="")
    region = models.CharField(max_length=4, default="0")
    country = models.CharField(max_length=16, default="mm")
    postal_code = models.CharField(max_length=12, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    read_only_fields = {
        "SDM":"",
        "ADM":"email",
            
    }  

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"
        ordering = ["id"]


class StudentWork(CustomModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    class Meta:
        verbose_name = "student_work"
        verbose_name_plural = "student_works"
        ordering = ["id"]



