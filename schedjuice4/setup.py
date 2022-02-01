import csv
import requests
import json
import random

from ms_stuff.graph_wrapper.mail import MailMS


AUTH = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyNzg5OTM0LCJpYXQiOjE2NDI3NzU1MzQsImp0aSI6IjIyN2U3MmY0MzgyYzQ1OTg4YTJiMGM2MjhhYTRkM2QzIiwidXNlcl9pZCI6NDZ9.AZpzwOQTErhsghfVyEOKvLIh2nN35iimFZh3Lpl-QSc"


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


def main():
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
            headers={"Authorization":"Bearer "+AUTH}
            )



def add_to_class(work,staff):
    data = {
        "work":work,
        "staff":staff
    }
    return requests.post(
            "http://localhost:8000/api/v1/studentworks",
            data=data,
            headers={"Authorization":"Bearer "+AUTH}
            )


