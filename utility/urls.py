from django.urls import path
from utility import views


urlpatterns = [
    path("freetimes/work/<int:work_id>", views.FreeTimeWork.as_view()),
    path("freetimes/staff/<int:staff_id>", views.FreeTimeStaff.as_view()),
    
    
]