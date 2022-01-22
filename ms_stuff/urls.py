from django.urls import path, include
from ms_stuff import views

urlpatterns = [
    path("signin", views.SignIn.as_view()),
]