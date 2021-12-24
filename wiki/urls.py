from django.urls import path
from wiki import views 


urlpatterns = [
    
    path("topics", views.TopicList.as_view()),
    path("topics/<int:obj_id>", views.TopicDetails.as_view()),
    path("topictags", views.TopicTagList.as_view()),
    path("topictags/<int:obj_id>", views.TopicTagDetails.as_view()),
]