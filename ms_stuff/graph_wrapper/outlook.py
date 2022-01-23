from datetime import datetime
from .base import MSRequest

from django.utils import timezone

from django.conf import settings


class CalendarMS(MSRequest):
    pass



class EventMS(MSRequest):

    def __init__(self, user:str):
        self.user = user
        super().__init__()

    def create_event(self):
        data = {
            "subject":"Test",
            "body":{
                "contentType":"HTML",
                "content":"test event"
            },
            "start":{
                "dateTime":timezone.datetime(2022,1,24,16,40).isoformat(),
                "timeZone":"Asia/Singapore"
            },
            "end":{
                "dateTime":timezone.datetime(2022,1,24,18,40).isoformat(),
                "timeZone":"Asia/Singapore"
            },
            "attendees":[
                {
                    "type":"required",
                    "emailAddress":{
                        "name":"staffy@teachersucenter.com"
                    }
                }
            ],
            "isOnlineMeeting": True,
            "onlineMeetingProvider": "teamsForBusiness",
            "allowNewTimeProposals":False
        }
        return self.post("users/"+"james@teachersucenter.com"+"/events",data)


    def get_schedule(self):
        data = {
            "schedules":["james@teachersucenter.com","staffy@teachersucenter.com"],
            "startTime":{
                "dateTime":datetime(2022,1,20).isoformat(),
                "timeZone":"Asia/Singapore"
            },
            "endTime":{
   
                "dateTime":datetime(2022,1,28).isoformat(),
                "timeZone":"Asia/Singapore"
            
            }
        }
        return self.post("users/james@teachersucenter.com/calendar/getSchedule",data)




    