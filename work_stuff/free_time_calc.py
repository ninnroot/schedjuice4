from work_stuff.models import Work, StaffSession, Session, StaffWork
from staff_stuff.models import Staff



def is_free(staff:Staff,session:Session):

    # check if works overlap
    works = StaffWork.objects.filter(staff=staff, status="active").all()

    for i in works:
        if i.valid_to > session.work.valid_from:
            sessions = Session.objects.filter(work=i,staff=staff).all()
            
            for j in sessions:
                if j.time_to > session.time_from:
                    return False

    return True











