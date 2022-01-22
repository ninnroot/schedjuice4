# schedjuice4

## A brief description
Schejuice 4 is an API for my school/work's staff management system as well as my passion project. This is built using the Django framework.
As the name suggests, this is the fourth iteration of the "idea": the idea of a management system that is. This should be final version of the idea.
After this, I would like to pursue other areas of studies rather than web development (at least the web development in Python).
This is built to be highly maintainable and scalable and to last througout the ages (at least I hope).  

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
Celery 

# External references and documentations
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