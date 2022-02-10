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

from . import default_obj

ENDPOINT = "https://localhost:8000/api/v1/"

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

def email_creator(name:str, controller:int):
    legal_chars = "abcdefghijklmnopqrstuvwxyz.0123456789"
    email = ""
    for i in name.split():
        if controller == 0 or controller == 1:
            c = ""
            for j in i.lower():
                if j in legal_chars:
                    c+=j
            email+=c
        else:
            c=""
            for j in i.lower():
                if j in legal_chars:
                    c+=j
            email+=c[0]
    email+=str(controller%15)
    return email

def get_ready_accounts():
    x = csv.reader(open('accounts.csv',"r"))
    x = [i for i in x]
    
    lst = []
    c = 0
    for i in x:
        e=email_creator(i[0],c)
        pw = password_create()

        y = [i[0], i[1], e+"@teachersucenter.com", pw, e]
        lst.append(y)

        c+=1
    csv.writer(open("readyaccounts.csv","w")).writerows(lst)

def create_staff():
    token = get_token()
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
                ENDPOINT+"staff",
                data=data,
                headers={"Authorization":"Bearer "+token}
                )

            if res.status_code not in range(199,300):
                print(f"ERROR in {c}\n",res.content)
                break

            print(f"LOG:\t{c}\t",res.content,"\n")
            print("===========\n\n")
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
            e=email_creator(i[0],c)
            lst = [
                i[0],
                i[1],
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
            ENDPOINT+"studentworks",
            data=data,
            headers={"Authorization":"Bearer "+token}
            )


def create_students(class_id, initial=True):
    token = get_token()
    x = csv.reader(open("readystudents.csv"))

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
                ENDPOINT+"students",
                data=data,
                headers={"Authorization":"Bearer "+token}
                )

            if res.status_code not in range(199,300):
                print(f"ERROR in {c}\n",res.content)
                break

            print(f"LOG:\t{c}\t",res.content,"\n")
            
            add = add_to_class(class_id,res.json()["id"],token)
            print("CLASS: ",add.content,"\n")
            c+=1
            print("===========\n\n")


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
    roles = default_obj.roles
    
    for i in roles:
        x=Role.objects.create(
            name=i["name"],
            shorthand=i["shorthand"],
            is_specific=i["is_specific"],
            deletable=False
        )
        x.save()
        print(i)

def add_to_trial():
    token = get_token()

    for i in Staff.objects.all():
            data = {
            "staff":i.id,
            "work":120,
            }

            res = requests.post("http://localhost:8000/api/v1/staffworks",
                    data,headers={"Authorization":"Bearer "+token})
            
            print(res.content)

