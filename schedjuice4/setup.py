import csv
import requests
import json
import random

from ms_stuff.graph_wrapper.mail import MailMS
from staff_stuff.models import Staff
from rest_framework_simplejwt.tokens import RefreshToken
from ms_stuff.exceptions import MSException

from work_stuff.models import Work
from student_stuff.models import Student
from role_stuff.models import Role


def password_create():
    a = "abcdefghijklmnopqrsquvwxyz"
    b = "1234567890"
    c = "!@#$"

    pw = "ts"

    for i in range(2):
        pw+=random.choice(a)
        pw+=random.choice(b)
        pw+=random.choice(c)
    pw+=random.choice(a).upper()

    return pw


def get_token():
    x = Staff.objects.get(email="james@teachersucenter.com")
    return str(RefreshToken.for_user(x).access_token)



def get_ready_accounts():
    x = csv.reader(open('accounts.csv',"r"))
    x = [i for i in x]
    
    lst = []
    c = 0
    for i in x:
        e=""

        cc = 0
        for j in i[0].split():
            if cc == 0 or cc ==1:
                e+=j.lower()
            else:
                e+=j[0].lower()
            cc+=1

        e+=str(c%15)
        
        pw = password_create()

        y = [i[0], i[1], e+"@teachersucenter.com", pw, e]
        lst.append(y)

        c+=1

    output = csv.writer(open("readyaccounts.csv","w"))
    output.writerows(lst)



def create_staff():
    token = get_token()
    m = MailMS()
    x = csv.reader(open("readyaccounts.csv","r"))
    
    c = 0
    for i in x:
        if i != []:
            data = {
                "email":i[2],
                "password":i[3],
                "uname":i[4],
                "dname":i[0],
                "gmail":i[1]
            }

            res = requests.post(
                "http://localhost:8000/api/v1/staff",
                data=data,
                headers={"Authorization":"Bearer "+token}
                )

            print("LOG: ",c,res.content)

            # res = m.send_welcome("staffy@teachersucenter.com",i[1],
            # {"name":i[0],"password":i[3],"email":i[2]})

            c+=1


def delete_staff():
    ban = ["james","heinthanth","su","staffy","albert","bruce"]
    ban = [i+"@teachersucenter.com" for i in ban]

    x = Staff.objects.all()
    for i in x:
        if i.email not in ban:
            
            print(i.delete(silent=False))


def get_std_acc(initial=True):
    x = csv.reader(open("students.csv","r"))
    y = csv.writer(open("readystudents.csv","w"))

    if initial:
        c=0
        for i in x:
            e=""

            cc = 0
            for j in i[0].split():
                if cc == 0 or cc ==1:
                    e+=j.lower()
                else:
                    e+=j[0].lower()
                cc+=1

            e+=str(c%15)

            lst = [
                i[0],
                i[3],
                e+"@teachersucenter.com",
                password_create(),
                e
            ]
            y.writerow(lst)
            c+=1
        

def add_to_class(work,student, token):
    data = {
        "work":work,
        "student":student
    }
    return requests.post(
            "http://localhost:8000/api/v1/studentworks",
            data=data,
            headers={"Authorization":"Bearer "+token}
            )


def create_students(class_id, initial=True):
    token = get_token()
    x = csv.reader(open("readystudents.csv"))
    m=MailMS()
    if initial:
        c=0
        for i in x:
            if i == []:
                continue

            data = {
                "dname":i[0],
                "email":i[2],
                "password":i[3],
                "uname":i[4],
                "gmail":i[1]
            }
            res = requests.post(
                "http://localhost:8000/api/v1/students",
                data=data,
                headers={"Authorization":"Bearer "+token}
                )

            print("LOG: ",c,res.content)
            print("\n")
            if res.status_code in range(199,300):
                add = add_to_class(class_id,res.json()["id"],token)
                print("CLASS: ",add.content)

            m.send_welcome("staffy@teachersucenter.com","tinwinnaing6969@gmail.com",
            {"name":i[0],"email":i[2],"password":i[3]})

            c+=1
            print("===========")


def delete_students():
    x = Student.objects.all()
    for i in x:
        print(i)
        i.delete(silent=False)
        
def create_works():
    token = get_token()
    x= csv.reader(open("works.csv","r"))
    for i in x:
        data = {
            "name":i[0],
            "valid_from":i[2],
            "valid_to":i[3],
        }
        res = requests.post("http://localhost:8000/api/v1/works",
        data,headers={"Authorization":"Bearer "+token})
        print("LOG: ",res.content)

        for j in i[1]:
  
            ses = {
                "work":res.json()["id"],
                "day":j,
                "time_from":i[4],
                "time_to":i[5]
            }
            res2 = requests.post("http://localhost:8000/api/v1/sessions",
            ses,headers={"Authorization":"Bearer "+token})
            print("SES: ",res2.content)

        print("========\n")

def delete_works():
    x=Work.objects.all()
    for i in x:
        try:
            i.delete(silent=False)
        except MSException:
            i.delete(silent=True)
            pass

def create_roles():
    roles = [
        {
            "name":"Superadmin",
            "shorthand":"SDM",
            "is_specific":False,
        },
        {
            "name":"Admin",
            "shorthand":"ADM",
            "is_specific":False,
        },
        {
            "name":"User",
            "shorthand":"USR",
            "is_specific":False,
        },
        {
            "name":"Main Teacher",
            "shorthand":"mtr",
            "is_specific":True,
        },
        {
            "name":"Assistant Teacher",
            "shorthand":"atr",
            "is_specific":True,
        },
        {
            "name":"Coordinator",
            "shorthand":"cor",
            "is_specific":True,
        },
        {
            "name":"Academic Director",
            "shorthand":"adr",
            "is_specific":True,
        },
    ]
    for i in roles:
        x=Role.objects.create(
            name=i["name"],
            shorthand=i["shorthand"],
            is_specific=i["is_specific"],
            deletable=False
        )
        x.save()
        print(i)






