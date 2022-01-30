from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response,status

from rest_framework.permissions import IsAuthenticated
from role_stuff.permissions import StatusCheck

from work_stuff.free_time_calc import get_schedule
from work_stuff.models import StaffWork, Work
from staff_stuff.models import Staff

from datetime import date


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
        