from django.db import models
from datetime import date, time

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from .managers import UserManager

from role_stuff.models import Role

from ms_stuff.graph_wrapper.user import UserMS
from ms_stuff.exceptions import MSException

from schedjuice4.models import CustomModel
from rest_framework.serializers import ValidationError



class Department(CustomModel):

    name = models.CharField(max_length=256, unique=True)
    shorthand = models.CharField(unique=True,max_length=6)
    description = models.TextField()
    is_under = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    read_only_fields = {
        "SDM":[],
        "ADM":["created_at","updated_at"]
    }

    class Meta:
        verbose_name = 'department'
        verbose_name_plural = 'departments'
        ordering = ["id"]



class Staff(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True)
    gmail = models.EmailField(unique=True,null=True)
    ms_id = models.CharField(max_length=256, unique=True)
    dname = models.CharField(max_length=128, default="Display Name")
    ename = models.CharField(max_length=128, default="Nickname")
    uname = models.SlugField(max_length=128, unique=True, validators=[RegexValidator(r"^[a-zA-Z0-9_]*$")])
    description = models.TextField(default="Description...")
    # statues = ["in progress", "unapproved","active","retired","on leave"]
    status = models.CharField(max_length=128, default="in progress")
    dob = models.DateField(default=date(2000,1,1))
    gender = models.CharField(max_length=16,default="")
    ph_num = models.CharField(max_length=60,default="09650222", validators=[RegexValidator(r'^\d{1,11}$')])
    facebook = models.CharField(max_length=256, default="https://facebook.com/profile")
    
    house_num = models.CharField(max_length=16, default="")
    street = models.CharField(max_length=128, default="")
    township = models.CharField(max_length=128, default="")
    city = models.CharField(max_length=128, default="")
    region = models.CharField(max_length=8, default="0")
    country = models.CharField(max_length=16, default="mm")
    postal_code = models.CharField(max_length=12, default="")

    profile_pic = models.ImageField(default="profile_pics/default.jpg", upload_to="profile_pics") 
    cover_pic = models.ImageField(default="cover_pics/default.jpg", upload_to="cover_pics")
    card_pic = models.ImageField(default="card_pics/default.jpg", upload_to="card_pics")
    first_day = models.DateField(default=date(2018,1,1))
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL, default=3)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    read_only_fields = {
        "SDM":[],
        "ADM":[
            "email",
            "uname",
            "description",
            "dob",
            "gender",
            "ph_num",
            "facebook",
            "region",
            "profile_pic",
            "cover_pic",
            "card_pic",
            "created_at",
            "updated_at"
        ],
        "USR":[
            "email",
            "uname",
            "status",
            "role",
            "house_num",
            "street",
            "township",
            "city",
            "region",
            "postal_code",
            "created_at",
            "updated_at",

        ]
    }

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staff members'
        ordering = ["id"]


    def delete(self, *args, **kwargs):
        # deleting MS account
        try:
            silent = kwargs.pop("silent")
            loud = not silent

            if loud:

                res = UserMS(self.email).delete()
            
                if res.status_code not in range(199,300):
                    raise MSException(detail=res.json())
                    
            return super().delete(*args, **kwargs)

        except KeyError:
            pass


class Tag(CustomModel):

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(default="Description...")
    color = models.CharField(max_length=7, default="#000000")
    deletable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    read_only_fields = {
        "SDM":[],
        "ADM":[
            "created_at",
            "updated_at",
        ],
    }
    def delete(self,*args,**kwargs):
        if not self.deletable:
            raise ValidationError("This is a system tag and cannot be deleted.")

        return super().delete(*args,**kwargs)
    
    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ["-id"]



class StaffDepartment(CustomModel):
    
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    pos = models.IntegerField()
    job = models.CharField(max_length=256,default="member")
    is_primary = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    read_only_fields = {
        "SDM":[],
        "ADM":[
            "created_at",
            "updated_at"
        ]
    }

    class Meta:
        verbose_name = "staffdepartment relation"
        verbose_name_plural = "staffdepartment relations"
        
        ordering = ["-id"]



class StaffTag(CustomModel):

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    pos = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    read_only_fields = {
        "SDM":[],
        "ADM":[
            "created_at",
            "updated_at"
        ]
    }

    class Meta:
        verbose_name = "stafftag relation"
        verbose_name_plural = "stafftag relations"
        
        ordering = ["-id"]
