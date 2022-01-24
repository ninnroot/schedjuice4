# schedjuice4

## A brief description
Schejuice 4 is an API for my school/work's staff management system as well as my passion project. This is built using the Django framework.
As the name suggests, this is the fourth iteration of the "idea": the idea of a management system that is.

This should be the final version of the idea.
After this, I would like to pursue other areas of studies rather than web development (at least the web development in Python).
This is built to be highly maintainable and scalable and to last througout the ages (at least I hope).  

The frontend of this api can be found [here](https://github.com/teachersucenter/simp-v2). It was developed by my amazing tech team from [teachersucenter](https://www.teachersucenter.com).

## Installation
The installation is straight-forward. It's just a normal Django project. For best practices, __you should use a virtual environment__.

### making virtual environment

__windows__
```
virtualenv env
env\\Scripts\\activate.bat

```

__mac__
```
virtualenv env
source env/bin/activate
```

### running the project
```
mkdir <directory-name>
cd <directory-name>
git clone https://github.com/Ninroot-Eater/schedjuice4.git
cd schedjuice4
pip install -r requirements.txt
python manage.py runserver
```

## Installation for celery
Celery is a task queue/job queue based on distributed message passing. It is focused on real-time operation, but supports scheduling as well. Read more [here](https://docs.celeryproject.org/projects/django-celery/en/2.4/introduction.html).

What I essentially wanted to do was to schedule certain tasks, like sending a reminder email. Now, with the integrations with Microsoft's Graph API, the [reminder](./reminder) app is not that useful anymore. 

You will need __redis__ to run celery. And, afterwards, two commands need to be ran. One for celery's asynchronous tasks, and the other called "celery beat" for scheduling. The latter is not working in Windows systems.

### commands to run a celery worker and a celery beat
```
celery -A schedjuice4 worker -l INFO
```
```
celery -A schedjuice4 beat -l INFO
```

## Request headers
For every request, an authorization header with a Bearer token. must be provided. See [here](#Authentication) on how to obtain it.
```http
Authorization: Bearer <token>
```


## Filtering and specifying fields
You can filter what kind of instances you want to receive.
```http
GET https://api.teachersucenter.com/api/v1/staff?x=Foo&y=Bar
```


You can also specify which fields you want in the response (so that the response body won't be large). By default, the server will return every field. For performance reason, I highly recommend to specify the fields you want to obtain.
```http
GET https://api.teachersucenter.com/api/v1?fields=name,id,email
```


## Authentication
Authentication is simple. Microsoft's Graph API handled most of it. However, [we](https://github.com/teachersucenter) only use MS mostly for authentication and application of its ohter services. What I am trying to say it, there are still a lot of data stored on our database. So, our own authentication is also still needed. (not sure how other do this. But, we came up with the following idea.)

##
- client side ask MS Graph for identity token
- client side request Schedjuice4 with the token
```javascript
axios.post(
    "https://api.teachersucenter.com/api/v1/signin",
    {"token":MS_token}
)
```
- Django accepts the request, make another request to MS with the obtained token
- find that user in the local database, generate a new JWT and responses with it
```python
class SignIn(APIView):
    def post(self, request):

        # request contains user's token obtained from client side
        token = request.data.get("token")

        if token is None:
            return Response({"error":"A token must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        
        # request made to MS api to know who the user is
        res = requests.get(
            constants["URL"]+"me",
            headers={"Authorization":"Bearer "+token, "Content-Type":"application/json"}
            )
        
        if res.status_code not in range(199,300):
            return Response({"MS_error":res.json()},status=status.HTTP_400_BAD_REQUEST)
        
        # get the user from local server's db
        id = res.json()["id"]
        user = Staff.objects.filter(ms_id=id).first()
        
        if user is None:
            return Response({"error":"No such SIMP user. This error shouldn't be possible actually."}, status=status.HTTP_404_NOT_FOUND)

        # generate access token for the user
        access = str(RefreshToken.for_user(user).access_token)

        return Response({"access":access},status=status.HTTP_200_OK)
```

## Authorization
Authentication was simple enough. The authorization part is more tricky. This is my first time developing a project of this scale. So, I am not very sure if I implemented the roles correctly. Shamelessly, I have to admit that I didnt' utlize Django's built-in roles and permissions. (But, I kinda used the permission classes.)

Roles are stored as instances in the database. There are some roles that have to be created at the start of the codebase. (I might write a setup.py for that in the future). The client can theoretically add more roles, but, they would only be for synthetic purposes as all the permissions are determined in the backend and they are all hard coded :< 

### Types of roles
Firstly, there are two types of roles: specific and non-specific roles. Specific roles determine what the user can do to the entire app as a whole. Non-specific ones determine what the user can do in a join-table (a relationship, like, a <code>Staff</code> object assigned to a <code>Work</code> object. You get what I mean). The specific roles' permissions can overwrite the non-specific ones'.

### Shorthands
Every role has a shorthand. They must be unique and consists only of 3 letters. Specific roles' shorthands are __uppercase__ and non-specific roles' shorthands are __lowercase__.


### Specific roles
There are three specific roles: Superadmin, Admin and User. Alternatively, you can remember them by thier __shorthands__: SDM, ADM and USR. The Superadmin can do anything. Staffy (a hypothetical persona (a user in this case) created during our projects) is the only one with the SDM role, and it's suiting, because, giving such power to a human would be a nightmare. So, Staffy is the only one I trust with the SDM role.

ADM role is given to administrators obviously. ADMs can assign <code>Staff</code>and <code>Students</code> to <code>Work</code>, <code>Departments</code> and <code>Sessions</code>, and <code>Work</code> to <code>Categories</code>. You get the idea. 

A USR can do everything else. They are the least powerful, representing an ordinary user. 


### Read-only fields
In addition to write and assigning permissions, the specific roles have differing writing access on an instance's individual field (i.e., a certain role won't be able to update a certain field). You can see each role's read-only fields in the each class in each models.py files. (I may list them here in the future. But, for now, the fields are not stable yet.)


### Excluded fields
This is similar with the read-only fields. But, the roles are not even allow to see them this time. 


### Non-specific roles
For now, non-specific roles are purely synthetic, so, from authorization purpose, you don't need to worry about this __yet__.
Here are current list of non-specific roles:
- Host (hos) (may get removed soon. idk)
- Main teacher (mtr)
- Assistant teacher (atr)
- Coordinator (cor)
- Academic director (adr)

or you can just send a GET request to <code>https://api.teachersucenter.com/api/v1/roles?specific=False</code>


***
<details>
<summary>External references and documentations</summary>
Development of schedjuice4 was my learning journey as much as it's a practical need for my work. The followings are some references that I found
and some new things I learnt. You will see a similar pattern in both the order of the addtion of the references here and my commits. 

## Setting up the Postgres database
This is something that you always have to do. So, better have a manual

see [here](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04)

## Storing historical data
Storing historical data with Django-reversion mixin for class-based views.

see [here](https://django-reversion.readthedocs.io/en/stable/views.html)

## User authentication and authorization
We need a convenient to manage persmissions and stuffs. Current solution is in a dire need of a good system.

see [here]( https://docs.djangoproject.com/en/3.2/topics/auth/default/)

## Websockets
idk it's cool. Might add it

see [here]( https://www.fullstackpython.com/websockets.html)

## Scheduling tasks, setting reminders
do this when it's Friday or something like that. Quite cool.

see [here](https://realpython.com/asynchronous-tasks-with-django-and-celery/) and
[here](https://docs.celeryproject.org/en/latest/userguide/)

## Email configuration
sending email using the app.

see [here](https://docs.djangoproject.com/en/3.2/topics/email/#topic-email-backends)

## Nested serializers
have related objects and stuffs configured using the serializers which is super cool.

see [here](https://stackoverflow.com/questions/14573102/how-do-i-include-related-model-fields-using-django-rest-framework)

## Django filter backend
enable filtering from url params with little code

see [here](https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend)

## Django REST API pagination
pagination, yea, pretty self-explanatory
see [here](https://stackoverflow.com/questions/59596342/django-rest-framework-custom-pagination-next-previous-links)

## Django write operations for nested serializers
add this staff to these classes IN A SINGLE REQUEST!

see [here](https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations)

## Google API without the client library
for FormAPI

see [here](https://stackoverflow.com/questions/50401755/requests-library-with-googleapiclient)

## Field specification
include or exclude fields with a query

see [here](https://stackoverflow.com/questions/23643204/django-rest-framework-dynamically-return-subset-of-fields)

## JWT token
authentication with JWT web tokens

see [here](https://simpleisbetterthancomplex.com/tutorial/2018/12/19/how-to-use-jwt-authentication-with-django-rest-framework.html) and
[here](https://medium.com/django-rest/django-rest-framework-jwt-authentication-94bee36f2af8)

## Optimizing SQL queries
neat ORM features to optimize query calls

see [here](https://www.citusdata.com/blog/2020/05/20/postgres-tips-for-django-and-python/)

## Fat models, thin views, alel
more encapsulation towards models. Another step in writing a scalable Django app

see [here](https://www.dabapps.com/blog/django-models-and-encapsulation/)

## Django Debug Toolbar
to optimize queries and to see what's actually happening underneath. This is the installation guide

see [here](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

## Django DRF permissions
yea, permissions

see [here](https://testdriven.io/blog/custom-permission-classes-drf/)

## Authentication with Microsoft
MS 365 migrations, yay!

see [here](https://docs.microsoft.com/en-us/graph/tutorials/python)

## MS Graph API docs
the docs are very helpful. 

see [here](https://docs.microsoft.com/en-us/graph/)

## For creating custom Exception classes
this is pretty easy. But, just for referencing matters.

see [here](https://www.django-rest-framework.org/api-guide/exceptions/#exceptions)

## Overriding predefined methods in Django models
another layer of encapsulation. I am falling in love with OOP.

see [here](https://docs.djangoproject.com/en/4.0/topics/db/models/#overriding-predefined-model-methods)

## Jinja2
to send emails in MIME format, I decided to add Jinja2 functionality and stuffs.

see [here](https://zetcode.com/python/jinja/) and [here](https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Template)

## MIME 
how MIME works while sending emails.

see [here](https://realpython.com/python-send-email/)

## Outlook calendar overview
just to help you get started on Outlook calendar.

see [here](https://docs.microsoft.com/en-us/graph/outlook-calendar-concept-overview)


</details>

