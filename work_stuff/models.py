from datetime import date, time
from django.db import models
from django.core.validators import RegexValidator
from staff_stuff.models import Staff
# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["-id"]



class Work(models.Model):

    name = models.CharField(max_length=256,unique=True)
    description = models.TextField(default="Description...")
    meeting_id = models.CharField(max_length=20,default="not provided",validators=[RegexValidator(r'^\d{1,11}$ ')])
    viber_group = models.CharField(max_length=256,default="https://")
    class_code = models.CharField(max_length=8, default="#code")
    valid_from = models.DateField(default=date(2000,1,1))
    valid_to = models.DateField(default=date(2000,12,1))
    # statuses = ["pending","active", "ended", "on halt"]
    status = models.CharField(max_length=32, default="active")
    predecessor = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    cover_pic = models.ImageField(default="work_covers/default.jpg", upload_to="work_covers")
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "work"
        verbose_name_plural = "works"
        ordering = ["-id"]


class Session(models.Model):

    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    day = models.CharField(max_length=1)
    time_from = models.TimeField(default=(time(16,0,0)))
    time_to = models.TimeField(default=time(18,0,0))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "session"
        verbose_name_plural = "sessions"
        ordering = ["-id"]



class StaffWork(models.Model):

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "staffwork relation"
        verbose_name_plural = "staffwork relations"
        ordering = ["-id"]


class StaffSession(models.Model):

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "staffsession relation"
        verbose_name_plural = "staffsession relations"
        ordering = ["-id"]


