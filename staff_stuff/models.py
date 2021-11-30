from django.db import models
from datetime import date, time
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.deletion import SET_NULL
from django.utils import timezone
from django.core.validators import RegexValidator
from .managers import UserManager





class Department(models.Model):

    name = models.CharField(max_length=256)
    is_under = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

class Staff(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True)
    dname = models.CharField(max_length=128, default="Display Name")
    ename = models.CharField(max_length=128, default="Nickname")
    description = models.TextField(default="Description...")
    dob = models.DateField(default=date(2000,1,1))
    gender = models.CharField(max_length=16,default="")
    ph_num = models.CharField(max_length=60,default="09650222", validators=[RegexValidator(r'^\d{1,11}$')])
    facebook = models.CharField(max_length=256, default="https://facebook.com/profile")
    region = models.CharField(max_length=8, default="0")
    profile_pic = models.ImageField(default="profile_pics/default.jpg", upload_to="profile_pics") 
    first_day = models.DateField(default=date(2018,1,1))

    department = models.ForeignKey(Department, null=True, on_delete=SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staff members'
        ordering = ["id"]

