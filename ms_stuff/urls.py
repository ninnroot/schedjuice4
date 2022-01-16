from django.urls import path, include
from ms_stuff import views

urlpatterns = [
    path("signin", views.SignIn.as_view()),
    path("signout", views.SignOut.as_view()),
    path("tokenurl", views.Redirected.as_view()),
    path("test",views.Test.as_view())
]