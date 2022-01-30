from work_stuff.models import Work, StaffSession, Session, StaffWork
from staff_stuff.models import Staff

from datetime import date, time, timedelta


def ftse(f,t,s,e):
    return (
        (f < s and f < e and t < s and t < e) or
        (f > s and f > e and t > s and t > e)
    )

def is_free(staff:Staff,session:Session):

    works = StaffWork.objects.filter(staff=staff).all()

    for i in works:
        if  ftse(i.work.valid_from, i.work.valid_to, session.work.valid_from, session.work.valid_to):
            sessions = Session.objects.filter(work=i.work).all().prefetch_related("work")
            
            for j in sessions:
                if StaffSession.objects.filter(session=j,staff=staff).first():
                    if not ftse(j.time_from, j.time_to, session.time_from, session.time_to):
                        return False

    return True


def is_session_collide(time_from,time_to, work:Work):
    
    sessions = Session.objects.filter(work=work)

    for i in sessions:
        if ftse(time_from,time_to,i.time_from,i.time_to):
            return False

    return True


def get_schedule(staff:Staff,start=None,end=None):
    
    if not start:
        start = date.today()
    if not end:
        end = start+timedelta(days=14)

    x = StaffSession.objects.filter(staff=staff).prefetch_related("session","staff")

    schedule = {}

    while start < end:
        y = []
        for i in x:

            
            if str(start.weekday()) == i.session.day:
                f = i.session.work.valid_from
                t = i.session.work.valid_to
                s = start
                e = end
                

                if not ftse(f,t,s,e):
                    
                    z = {
                        "time_from":i.session.time_from,
                        "time_to":i.session.time_to,
                        "day":start.weekday(),
                        "session":i.session.id,
                        "staffsession":i.id
                        }
                    y.append(z)

        if not start.isoformat() in schedule:
            schedule[start.isoformat()] = y
        else:
            schedule[start.isoformat()]+=y

        start += timedelta(days=1)

    return {"schedule":schedule}






