from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response,status

from rest_framework.permissions import IsAuthenticated
from role_stuff.permissions import StatusCheck, IsADMOrReadOnly

from work_stuff.free_time_calc import get_schedule
from work_stuff.models import StaffWork, Work, StaffSession, Session
from staff_stuff.models import Staff

from datetime import date, timedelta, datetime
import numpy as np
from dateutil import relativedelta
import csv


class FreeTimeWork(APIView):
    permission_classes = [IsAuthenticated, StatusCheck]

    def get(self, request, work_id):
        start = request.query_params.get("start")
        if start:
            try:
                start = date.fromisoformat(start)

            except ValueError:
                return Response({"error":"Improper query param"},status=status.HTTP_400_BAD_REQUEST)

        end = request.query_params.get("end")
        if end:
            try:
                end = date.fromisoformat(end)

            except ValueError:
                return Response({"error":"Improper query param"},status=status.HTTP_400_BAD_REQUEST)


        lst = []
        work = get_object_or_404(Work, pk=work_id)
        x = StaffWork.objects.filter(work=work).all().prefetch_related("staff","work")
        for i in x:
            lst.append({"staff":i.id,"schedule":get_schedule(i.staff,start, end)})

        return Response(lst,status=status.HTTP_200_OK)
        


class FreeTimeStaff(APIView):
    permission_classes = [IsAuthenticated, StatusCheck]

    def get(self, request, staff_id):

        start = request.query_params.get("start")
        if start:
            try:
                start = date.fromisoformat(start)

            except ValueError:
                return Response({"error":"Improper query param"},status=status.HTTP_400_BAD_REQUEST)

        end = request.query_params.get("end")
        if end:
            try:
                end = date.fromisoformat(end)

            except ValueError:
                return Response({"error":"Improper query param"},status=status.HTTP_400_BAD_REQUEST)

        staff = get_object_or_404(Staff, pk=staff_id)

        return Response(get_schedule(staff,start,end),status=status.HTTP_200_OK)



class PayrollReport(APIView):
    pays = {
        "yl":6571,
        "isf":9375,
        "isp":37500
    }
    days = {"0":"Mon","1":"Tue","2":"Wed","3":"Thu","4":"Fri","5":"Sat","6":"Sun"}
    #permission_classes = [IsAuthenticated, StatusCheck, IsADMOrReadOnly]
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        x = datetime.now() + relativedelta.relativedelta(months=1)
        s = x.date().isoformat().split("-")[0]+"-"+x.date().isoformat().split("-")[1]
        x = x + relativedelta.relativedelta(months=1)
        e = x.date().isoformat().split("-")[0]+"-"+x.date().isoformat().split("-")[1]

        dd = {k:np.busday_count(s,e,self.days[k]) for k in self.days}
        allstaff = Staff.objects.all().prefetch_related(
            
            "stafftag_set",
            "staffdepartment_set__job",
            "user_permissions",
            "groups",
            "role",
     
            "staffwork_set__role"
            )
        allsessions = StaffSession.objects.all().prefetch_related(
            "staff",
            "role",
            "session",
        
            "session__work__category",
        )
        allwork = StaffWork.objects.all().prefetch_related(
            "staff",
            "work",


        )
        lst = []
        for i in allstaff:
            staff = {"id":i.id,"name":i.dname,"email":i.email,"works":[],"salary":0}
            
            for a in allwork:
                if i.id == a.staff.id:
                    
                    x = {"class_name":a.work.name,"sessions":[],"total":0}
                    for j in allsessions:
                        if i.id==j.staff.id and j.role.shorthand in ["atr","clr"] and j.session.work.id==a.work.id:
                            m = 0
                            if j.session.work.category.name in ["IELTS"]:
                                m+=self.pays["isf"]*dd[j.session.day]
                            elif j.session.work.category.name in ["Preparation/Booster"]:
                                m+=self.pays["isp"]*dd[j.session.day]
                            else:
                                m+=self.pays["yl"]*dd[j.session.day]
                            staff["salary"]+=m
                            x["total"]+=m
                            x["sessions"].append({"day":self.days[j.session.day],"time":f"{j.session.time_from}-{j.session.time_to}","money":m})
                    staff["works"].append(x)
            lst.append(staff)
        

        return Response(lst,status=status.HTTP_200_OK)