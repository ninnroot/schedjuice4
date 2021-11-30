from django.urls import path, include
from staff_stuff import views

urlpatterns = [
    path("staff", views.StaffList.as_view()),
    path("staff/<int:obj_id>", views.StaffDetails.as_view()),
    path("department", views.DepartmentList.as_view()),
    path("department/<int:obj_id>", views.DepartmentDetails.as_view())
]