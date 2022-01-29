from datetime import date, time
from http.client import BAD_REQUEST
from django.db import models
from django.core.validators import RegexValidator

from staff_stuff.models import Staff
from role_stuff.models import Role

from ms_stuff.graph_wrapper.group import GroupMS
from ms_stuff.graph_wrapper.outlook import EventMS

from schedjuice4.models import CustomModel
from ms_stuff.exceptions import MSException



class Category(CustomModel):

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    read_only_fields = {
        "SDM":[],
        "ADM":[
            "name",
            "created_at",
            "updated_at"
        ]
    }

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["-id"]



class Work(CustomModel):

    name = models.CharField(max_length=256,unique=True)
    ms_id = models.CharField(max_length=256, unique=True)
    description = models.TextField(default="Description...")
    organizer = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    valid_from = models.DateField(default=date(2000,1,1))
    valid_to = models.DateField(default=date(2000,12,1))
    # statuses = ["pending", "ready" ,"active", "ended", "on halt"]
    status = models.CharField(max_length=32, default="active")
    predecessor = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    cover_pic = models.ImageField(default="work_covers/default.jpg", upload_to="work_covers")
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    read_only_fields = {
        "SDM":[],
        "ADM":[
            "created_at",
            "updated_at"
        ],
        "USR":[
            "name",
            "valid_from",
            "valid_to",
            "status",
            "predecessor",
            "category",
            "created_at",
            "updated_at"
        ]
    }

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    
    def delete(self, *args, **kwargs):
        
        # deleting MS team
        silent = False
        if "silent" in kwargs:
            silent = kwargs.pop("silent")

        if not silent:
            
            # "r" should be in kwargs. It's called privately anyway.
            r = kwargs.pop("r")
            res = GroupMS(self.ms_id).delete()
        

            if res.status_code not in range(199,300):
                raise(MSException(detail=res.json()))
            
        return super().delete(*args, **kwargs)


    class Meta:
        verbose_name = "work"
        verbose_name_plural = "works"
        ordering = ["-id"]


class Session(CustomModel):

    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    day = models.CharField(max_length=1)
    time_from = models.TimeField(default=(time(16,0,0)))
    time_to = models.TimeField(default=time(18,0,0))
    event_id = models.CharField(unique=True, max_length=256)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    read_only_fields = {
        "SDM":[],
        "ADM":[
            "created_at",
            "updated_at"
        ],
        "USR":[
            "work",
            "day",
            "time_from"
            "time_to",
            "created_at",
            "updated_at"
        ]
    }


    def __str__(self):
        return f"{self.work}:{self.day}:{self.time_from}-{self.time_to}"
        

    def delete(self, *args, **kwargs):
        if not kwargs.pop("silent"):
            res = EventMS(self.event_id,self.work.organizer.email).delete()
            if res.status_code not in range(199,300):
                raise MSException(res.json())  

        return super().delete(*args, **kwargs)


    class Meta:
        verbose_name = "session"
        verbose_name_plural = "sessions"
        ordering = ["-id"]



class StaffWork(CustomModel):

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    read_only_fields = {
        "SDM":[],
        "ADM":["created_at","updated_at"],
        "USR":["staff","work","role","created_at","updated_at"]
    }

    class Meta:
        verbose_name = "staffwork relation"
        verbose_name_plural = "staffwork relations"
        ordering = ["-id"]


class StaffSession(CustomModel):

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    read_only_fields = {
        "SDM":[],
        "ADM":["created_at","updated_at"],
        "USR":["staff","session","role","created_at","updated_at"]
    }

    def delete(self, *args, **kwargs):
        
        res = EventMS(
            self.session.event_id, self.session.work.orgaizer.email
        ).remove_attendee(self.staff,self.objects.filter(session=self.session).all())
        if res.status_code not in range(199,300):
            raise MSException(res.json())

        return super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "staffsession relation"
        verbose_name_plural = "staffsession relations"
        ordering = ["-id"]


