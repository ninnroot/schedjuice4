from django.urls import path, include
from work_stuff import views


urlpatterns = [
    path("categories", views.CategoryList.as_view()),
    path("categories/<int:obj_id>", views.CategoryDetails.as_view()),
    path("works", views.WorkList.as_view()),
    path("works/<int:obj_id>", views.WorkDetails.as_view()),
    path("works/search", views.WorkSearch.as_view()),
    path("sessions", views.SessionList.as_view()),
    path("sessions/<int:obj_id>", views.SessionDetails.as_view()),
    path("staffworks", views.StaffWorkList.as_view()),
    path("staffworks/<int:obj_id>", views.StaffWorkDetails.as_view()),
    path("staffsessions", views.StaffSessionList.as_view()),
    path("staffsessions/<int:obj_id>", views.StaffSessionDetails.as_view()),
    
]