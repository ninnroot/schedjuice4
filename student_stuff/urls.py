from django.urls import path, include
from student_stuff import views

urlpatterns = [
    path("students", views.StudentList.as_view()),
    path("students/<int:obj_id>", views.StudentDetails.as_view()),
    path("studentworks", views.StudentWorkList.as_view()),
    path("studentworks/<int:obj_id>", views.StudentWorkDetails.as_view()),
    path("students/search",views.StudentSearch.as_view())
    
]