from django.urls import path, include
from work_stuff import views


urlpatterns = [
    path("work", views.WorkList.as_view()),
    path("work/<int:obj_id>", views.WorkDetails.as_view()),
    path("session", views.SessionList.as_view()),
    path("session/<int:obj_id>", views.SessionDetails.as_view()),
    path("staffwork", views.StaffWorkList.as_view()),
    path("staffwork/<int:obj_id>", views.StaffWorkDetails.as_view()),
    path("staffsession", views.StaffSessionList.as_view()),
    path("staffsession/<int:obj_id>", views.StaffSessionDetails.as_view()),

 
    
]