import imp
import requests
import json

URL = "https://graph.microsoft.com/v1.0/"

def get_user(token):
    user = requests.get(
        URL+"me",
        headers={"Authorization":"Bearer "+token}
    )
    return user.json()

def get_calendar_events(token, start, end, timezone):
    headers = {
        "Authorization": "Bearer "+ token,
        "Prefer":"outlook.timezone="+timezone
    }
    query_params = {
        'startDateTime': start,
        'endDateTime': end,
        '$select': 'subject,organizer,start,end',
        '$orderby': 'start/dateTime',
        '$top': '50'
        }

    events = requests.get(
        URL+"me/calendarview",
        headers=headers,
        params=query_params
    )

    return events.json()

