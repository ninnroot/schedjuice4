from django.urls import path, include
from staff_stuff import views

urlpatterns = [
    path("staff", views.StaffList.as_view()),
    path("staff/<int:obj_id>", views.StaffDetails.as_view()),
    path("staff/search", views.StaffSearch.as_view()),
    path("departments", views.DepartmentList.as_view()),
    path("departments/<int:obj_id>", views.DepartmentDetails.as_view()),
    path("tags", views.TagList.as_view()),
    path("tags/<int:obj_id>", views.TagDetails.as_view()),
    path("jobs", views.JobList.as_view()),
    path("jobs/<int:obj_id>", views.JobDetails.as_view()),
    path("staffdepartments", views.StaffDepartmentList.as_view()),
    path("staffdepartments/<int:obj_id>", views.StaffDepartmentDetails.as_view()),
    path("stafftags", views.StaffTagList.as_view()),
    path("stafftags/<int:obj_id>", views.StaffTagDetails.as_view())
]