from django.urls import path, include
from staff_stuff import views

urlpatterns = [
    path("staff", views.StaffList.as_view()),
    path("staff/<int:obj_id>", views.StaffDetails.as_view()),
    path("department", views.DepartmentList.as_view()),
    path("department/<int:obj_id>", views.DepartmentDetails.as_view()),
    path("tag", views.TagList.as_view()),
    path("tag/<int:obj_id>", views.TagDetails.as_view()),
    path("staffdepartment", views.StaffDepartmentList.as_view()),
    path("staffdepartment/<int:obj_id>", views.StaffDepartmentDetails.as_view()),
    path("stafftag", views.StaffTagList.as_view()),
    path("stafftag/<int:obj_id>", views.StaffTagDetails.as_view())
]