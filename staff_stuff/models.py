from django.db import models
from datetime import date, time
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from .managers import UserManager

class Department(models.Model):

    name = models.CharField(max_length=256, unique=True)
    shorthand = models.CharField(unique=True,max_length=6)
    description = models.TextField()
    is_under = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'department'
        verbose_name_plural = 'departments'
        ordering = ["id"]

class Staff(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True)
    dname = models.CharField(max_length=128, default="Display Name")
    ename = models.CharField(max_length=128, default="Nickname")
    uname = models.SlugField(max_length=128, unique=True, validators=[RegexValidator(r"^[a-zA-Z0-9_]*$")])
    description = models.TextField(default="Description...")
    # statues = ["in progress:0-3", "unapproved","active","retired","on leave"]
    status = models.CharField(max_length=128, default="unapproved")
    dob = models.DateField(default=date(2000,1,1))
    gender = models.CharField(max_length=16,default="")
    ph_num = models.CharField(max_length=60,default="09650222", validators=[RegexValidator(r'^\d{1,11}$')])
    facebook = models.CharField(max_length=256, default="https://facebook.com/profile")
    region = models.CharField(max_length=8, default="0")
    profile_pic = models.ImageField(default="profile_pics/default.jpg", upload_to="profile_pics") 
    cover_pic = models.ImageField(default="cover_pics/default.jpg", upload_to="cover_pics")
    card_pic = models.ImageField(default="card_pics/default.jpg", upload_to="card_pics")
    first_day = models.DateField(default=date(2018,1,1))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staff members'
        ordering = ["id"]

class Tag(models.Model):

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(default="Description...")
    color = models.CharField(max_length=7, default="#000000")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ["-id"]

class StaffDepartment(models.Model):
    
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    pos = models.IntegerField()
    is_primary = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "staffdepartment relation"
        verbose_name_plural = "staffdepartment relations"
        
        ordering = ["-id"]


class StaffTag(models.Model):

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    pos = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "stafftag relation"
        verbose_name_plural = "stafftag relations"
        
        ordering = ["-id"]
