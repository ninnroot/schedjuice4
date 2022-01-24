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
        self.headers["Prefer"]='outlook.timezone="Asia/Rangoon"'
        
    def create_event(self):
        data = {
            "subject":"Test2",
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
                        "address":"james@teachersucenter.com"
                    }
                }
            ],
            "isOnlineMeeting": True,
            "onlineMeetingProvider": "teamsForBusiness",
            "allowNewTimeProposals":False
        }
        return self.post("users/"+"staffy@teachersucenter.com"+"/events",data)


    def list_events(self):
        return self.get("users/"+self.user+"/events?$select=subject,start,end")

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




    