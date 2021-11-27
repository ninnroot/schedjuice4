from django.urls import path, include
from reminder import views

urlpatterns = [
    path("mailto", views.SendMail.as_view())
]