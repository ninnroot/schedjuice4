import csv
import requests
import json
import random
from datetime import date

from ms_stuff.graph_wrapper.mail import MailMS
from staff_stuff.models import Staff
from rest_framework_simplejwt.tokens import RefreshToken
from ms_stuff.exceptions import MSException

from work_stuff.models import Work
from student_stuff.models import Student
from role_stuff.models import Role

from ms_stuff.graph_wrapper.group import GroupMS
from ms_stuff.graph_wrapper.user import UserMS
from . import default_obj

ENDPOINT = "http://localhost:8000/api/v1/"

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
    s=0
    for i in name.split():
        if s == 0 or s == 1:
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
        s+=1
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


def get_std_acc(fname):
    x = csv.reader(open(fname,"r",encoding="utf-8"))
    y = csv.DictWriter(open(f"ready{fname}","w", encoding="utf-8"),
    [
        "dname",
        "ename",
        "email",
        "password",
        "gmail",
        "dob",
        "uname",
        "gender",
        "ph_num",
        "house_num",
        "street",
        "township",
        "city",
        "region"
        ])
    y.writeheader()
    
    c=0
    for i in x:
        t = [int(j) for j in i[2].split("/")]
        dob = date(t[2],t[1],t[0])
        e=email_creator(i[0],c)
        lst = {
            "dname":i[0],
            "ename":i[1],
            "email":e+"@teachersucenter.com",
            "password":password_create(),
            "dob":dob,
            "uname":e,
            "gender":i[3].lower(),
            "gmail":i[4],
            "ph_num":i[5].strip(),
            "house_num":i[7],
            "street":i[8],
            "township":i[9],
            "city":i[10],
            "region":i[11].split(".")[-1]
        }
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


def create_students(fname,class_id=None):
    token = get_token()
    x = csv.DictReader(open(f"ready{fname}",encoding="utf-8"))
    err = csv.writer(open(f"error{fname}","w",encoding="utf-8"))
    w=Work.objects.get(id=class_id).name
    c=0
    for i in x:
        if i == []:
            continue

        data = {**i}
        res = requests.post(
            ENDPOINT+"students",
            data=data,
            headers={"Authorization":"Bearer "+token}
            )

        if res.status_code not in range(199,300):
            print(f"ERROR in {c}\n",res.content)
            if res.status_code == 400:

                err.writerow([i["dname"],i["gmail"],w,res.json()])
                print("LOGGED")
                continue
            else:
                
                break

        print(f"LOG:\t{c}\t",res.content,"\n")
        
        if class_id:
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
        finally:
            print(i)

def create_roles():
    roles = default_obj.roles
    
    for i in roles:
        x=Role.objects.create(**i)
        x.save()
        print(i)


def create_tags():
    pass


def create_departments():
    x = default_obj.departments
    auth = get_token()
    c=1
    for i in x:
        data = {**i}
        res = requests.post(ENDPOINT+"departments",data,
        headers={"Authorization":"Bearer "+auth})
        
        print(f"LOG: {c}\t",res.json(),)
        c+=1


def create_categories():
    pass

def create_jobs():
    pass


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



def x():
    x=csv.reader(open("data.csv","r",encoding="utf-8"))
    x=[i for i in x]
    for i in x:
        if i == []:
            continue
        print(i)
        g=GroupMS(i[2])
        print("removing member")
        res= g.remove_member(i[1],"members")
        if res.status_code not in range(199,300):
            print("removing owner")
            res= g.remove_member(i[1],"owners")
        print(res.content)
        print("\nadding owner")
        m=UserMS(i[0]).add_to_group(i[1],i[2],"owners")
        print(m.content)
        print("SUCCESS: ",i)