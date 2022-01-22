import csv
import requests
import json

from ms_stuff.graph_helper import MailMS

SES = "n0wozpw0sxzwm8y7dcjf2uug33xbuz3x"
AUTH = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyNzg5OTM0LCJpYXQiOjE2NDI3NzU1MzQsImp0aSI6IjIyN2U3MmY0MzgyYzQ1OTg4YTJiMGM2MjhhYTRkM2QzIiwidXNlcl9pZCI6NDZ9.AZpzwOQTErhsghfVyEOKvLIh2nN35iimFZh3Lpl-QSc"


def main():
    x = csv.reader(open('accounts.csv',"r"))
    x = [i for i in x]
    
    lst = []
    c = 0
    for i in x:
        e=""

        cc = 0
        for j in i[1].split():
            if cc == 0:
                e+=j.lower()
            else:
                e+=j[0].lower()
            cc+=1

        e+=str(c%10)
        

        y = {"gmail":i[2],"name":i[1], "email":e+"@teachersucenter.com"}
        lst.append(y)

        c+=1

    return lst

def create():
    m = MailMS()

    for i in main():
        data = {
            "email":i["email"],
            "password":"dh#!fFO2f23#",
            "uname":i["email"].split("@")[0],
            "dname":i["name"]
        }
        res = requests.post(
            "http://localhost:8000/api/v1/staff",
            data=data,
            cookies={"sessionid":SES},
            headers={"Authorization":"Bearer "+AUTH}
            )
        if res.status_code not in range(199,300):
            print(res.content)

        s = res.json()["id"]
        res = add_to_class(14,s)
        if res.status_code not in range(199,300):
            print(res.json())

        context = {"name":i["name"], "email":i["email"], "password":"dh#!fFO2f23#"}
        res = m.send_welcome("staffy@teachersucenter.com",i["gmail"],context=context)
        if res.status_code not in range(199,300):
            print(res.json())
        print(i)


def add_to_class(work,staff):
    data = {
        "work":work,
        "staff":staff
    }
    return requests.post(
            "http://localhost:8000/api/v1/studentworks",
            data=data,
            cookies={"sessionid":SES},
            headers={"Authorization":"Bearer "+AUTH}
            )


def create_stu():
    pw = "hggODG37!@$"
    for i in main():
        data = {
            "email":i["email"],
            "dname":i["name"]
        }

        res = requests.post(
            "http://localhost:8000/api/v1/students",
            data=data,
            cookies={"sessionid":SES},
            headers={"Authorization":"Bearer "+AUTH}
            )
        if res.status_code not in range(199,300):
            print(res.content)

        s = res.json()["id"]
        res = add_to_class(14,s)
        if res.status_code not in range(199,300):
            print(res.content)

        context = {"name":i["name"], "email":i["email"], "password":pw}
        res = MailMS().send_welcome("staffy@teachersucenter.com",i["gmail"],context=context)
        res = MailMS().send_welcome("staffy@teachersucenter.com","tinwinnaing6969@gmail.com",context=context)
        if res.status_code not in range(199,300):
            print(res.content)
        print(i)

def mmsp():
    for i in main():
        pw = "hggODG37!@$"
        context = {"name":i["name"], "email":i["email"], "password":pw}
        res = MailMS().send_welcome("staffy@teachersucenter.com",i["gmail"],context=context)
        #res = MailMS().send_welcome("staffy@teachersucenter.com","tinwinnaing6969@gmail.com",context=context)
        print(i, res.status_code)