from datetime import datetime, timezone
import json

from .base import MSRequest
from ms_stuff.exceptions import WrapperException

from django.utils import timezone
from django.conf import settings

from staff_stuff.models import Staff



class CalendarMS(MSRequest):
    pass



class EventMS(MSRequest):

    api_timezone = "Asia/Singapore"

    def __init__(self, event:str, organizer_id:str):
        
        self.event = event
        self.organizer = organizer_id
        
        super().__init__()
        self.headers["Prefer"]='outlook.timezone="Asia/Rangoon"'


    @staticmethod
    def get_commons():
        return {
            "allowNewTimeProposals":False,
            "isOnlineMeeting":True,
            "onlineMeetingProvider":"teamsForBusiness"
        }


    @classmethod
    def time_maker(cls, session):
        x=session.time_from
        y = session.time_to
        a = session.work.valid_from
        x = datetime(a.year,a.month,a.day,x.hour,x.minute,x.second)
        y = datetime(a.year,a.month,a.day,y.hour,y.minute,y.second)
        
        tz = timezone.activate("Asia/Rangoon")
        time_from = (x.astimezone(tz))
        time_to = (y.astimezone(tz))


        return {
            "start":{
                "dateTime":time_from.isoformat(),
                "timeZone":cls.api_timezone
                },
            "end":{
                "dateTime":time_to.isoformat(),
                "timeZone":cls.api_timezone
                }
            }

    @classmethod
    def range_maker(cls, work):

        return {
            "type":"endDate",
            "startDate":work.valid_from.isoformat(),
            "endDate":work.valid_to.isoformat(),
            "recurrenceTimeZone":cls.api_timezone,
            "numberOfOccurrences":0
        }


    @classmethod
    def get_attendees(cls, query_set):
        
        x = query_set
        if x == []:
            raise WrapperException("No such session.")
        
        lst = []

        for i in x:
            lst.append({
                "emailAddress":{
                    "address":i.staff.email,
                    "name":i.staff.dname
                    },
                "type":"required"
                })

        return lst


    @classmethod
    def create_event_for_session(cls, session):
        cls.get_token()
        data = {
            "subject":str(session),
            "body":{
                "contentType":"HTML",
                "content":f"created by Schedjuice4 at {timezone.now()}"
            },
            "recurrence":{
                "pattern":{
                    "type":"weekly",
                    "interval":1,
                    "daysOfWeek":[cls.day_mapper[int(session.day)]]
                },
                "range":cls.range_maker(session.work),
            },
            "organizer":{
                "emailAddress":{
                    "address":session.work.organizer.email,
                    "name":session.work.organizer.dname
                }
            },

            # start and end time
            **cls.time_maker(session),

            # common properties
            **cls.get_commons()
        }
        x = open('mmsp.json',"w").write(json.dumps(data))
        
        return cls.post(f"users/{session.work.organizer.ms_id}/calendar/events",data)
        

    def add_attendee(self, attendee, session, query_set):

        data = {
            "attendees":self.get_attendees(session, query_set) + {
                "emailAddress":{
                    "address":attendee.email,
                    "name":attendee.dname
                },
                "type":"required"
            }
        }

        return self.patch(f"users/{self.organizer}/events/{self.event}", data)

    
    def remove_attendee(self, attendee, session, query_set):

        lst = []
        for i in self.get_attendees(session, query_set):
            if i["emailAddress"]["address"] != attendee.email:
                lst.append(i)

        data = {
            "attendees":lst
        }

        return self.patch(f"users/{self.organizer}/events/{self.event}", data)
    

    def delete(self):
        return super().delete(f"users/{self.organizer}/events/{self.event}")    


    