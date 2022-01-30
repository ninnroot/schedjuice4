from work_stuff.models import Work, StaffSession, Session, StaffWork
from staff_stuff.models import Staff

from datetime import date, time, timedelta



def is_free(staff:Staff,session:Session):

    works = StaffWork.objects.filter(staff=staff).all()

    for i in works:
        if i.work.valid_to > session.work.valid_from:
            sessions = Session.objects.filter(work=i.work).all().prefetch_related("work","staff")
            
            for j in sessions:
                if StaffSession.objects.filter(session=j,staff=staff).first():
                    if j.time_to > session.time_from and j.time_to < session.time_to:
                        return False

    return True


def is_session_collide(time_to, work:Work):
    
    sessions = Session.objects.filter(work=work)

    for i in sessions:
        if i.time_to > time_to:
            return False

    return True


def get_schedule(staff:Staff,start=None,end=None):
    
    if not start:
        start = date.today()
    if not end:
        end = start+timedelta(days=7)

    x = StaffSession.objects.filter(staff=staff).prefetch_related("session","staff")

    schedule = {}

    while start < end:
        y = []
        for i in x:

            if i.session.day == str(start.weekday()):

                if i.session.work.valid_from > start and i.session.work.valid_from < end:
                    
                    z = {i.id:{
                        "time_from":i.session.time_from,
                        "time_to":i.session.time_to,
                        "date":start.isoformat()
                        }}
                    y.append(z)
        if not start.weekday() in schedule:
            schedule[start.weekday()] = y
        else:
            schedule[start.weekday()]+=y

        start += timedelta(days=1)

    return {"schedule":schedule}






