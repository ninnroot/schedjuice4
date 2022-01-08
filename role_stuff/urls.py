from django.urls import path
from role_stuff import views

urlpatterns = [
    path("roles", views.RoleList.as_view()),
    path("roles/<int:obj_id>", views.RoleDetails.as_view())
]