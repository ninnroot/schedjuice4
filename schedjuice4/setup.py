import csv
import requests
import json

from ms_stuff.graph_helper import MailMS

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

def create(lst):
    m = MailMS()

    for i in lst:
        data = {
            "email":i["email"],
            "password":"dh#!fFO2f23#",
            "uname":i["email"].split("@")[0],
            "dname":i["name"]
        }
        res = requests.post(
            "http://localhost:8000/api/v1/staff",
            data=data,
            cookies={"sessionid":"n0wozpw0sxzwm8y7dcjf2uug33xbuz3x"},
            headers={"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyNzAxMTE5LCJpYXQiOjE2NDI2ODY3MTksImp0aSI6IjM1OWExOTJiNmFkODRiMDE5NDM3MjIxMzdlMzdlNTI1IiwidXNlcl9pZCI6NDZ9.BlWDPwszu4jfLJieca-_aHhbK-mNoh7urfWvwSYCjUk"}
            )
        if res.status_code not in range(199,300):
            print(res.json())
        context = {"name":i["name"], "email":i["email"], "password":"dh#!fFO2f23#"}
        res = m.send_welcome("staffy@teachersucenter.com",i["gmail"],context=context)
        if res.status_code not in range(199,300):
            print(res.json())
        print(i)
