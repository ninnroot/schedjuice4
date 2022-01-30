from work_stuff.models import Work, StaffSession, Session, StaffWork
from staff_stuff.models import Staff



def is_free(staff:Staff,session:Session):

    works = StaffWork.objects.filter(staff=staff).all()

    for i in works:
        if i.work.valid_to > session.work.valid_from:
            sessions = Session.objects.filter(work=i.work).all()
            
            for j in sessions:
                if StaffSession.objects.filter(session=j,staff=staff).first():
                    if j.time_to > session.time_from:
                        return False

    return True


def is_session_collide(time_to, work:Work):
    
    sessions = Session.objects.filter(work=work)

    for i in sessions:
        if i.time_to > time_to:
            return False

    return True









