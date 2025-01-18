# DRF : Django Rest Framework
REST Framework built on Django



# Getting Started

## How to install
Just install ```django``` and ```djangorestframework```


## What will we use for testing

We will use ```curl``` to test API urls
```curl``` comes shipped with most OS, in case you don't have it you can download it from https://curl.haxx.se/

# Initializing Django project

First we will create a Django project and we will name it Fedora

```bash
django-admin startproject Fedor
```

Above will create a folder called ```Fedora``` which represents the project.
```Fedora``` project folder will contains ```manage.py``` that we will use to do many kinds of things like 
- creating default database such as auth
- creating a superuser
- creatings new apps

So we will go into ```Fedora``` folder and first run ```migrate``` to have database with default tables to hold users for instance.

```bash
python manage.py migrate
```

```bash
python manage.py createsuperuser
```

Next we will make a new django app called ```people```

```bash
python manage.py startapp people
```

# Change project settings to add rest_framework and people apps

We will make changes to the project ```settings.py``` file.
We will add ```127.0.0.1``` and ```localhost``` to ```ALLOWED_HOSTS```
so that we can access our applications.

We will register django rest framework and our newly made ```people``` app within ```INSTALLED_APPS```

```python
ALLOWED_HOSTS=["127.0.0.1","localhost"]
INSTALLED_APPS=["....","rest_framework","people"]
```

# Model and serializer
We will create a simple ```Person``` model with first, last and title fields.
We will then create a corresponding *serializer* for the ```Person``` model.
Serializer specifies how the model should be serialized into a payload.

Usually you create ```serializers.py``` file under the application folder and define serializers for each model

A convention for serializer is to name it as <Model name>Serializer.

You import ```serializers``` module from ```rest_framework``` and then create a class extending ```serializers.ModelSerializer```.

Below is simple example of defining a serializer for a model ```Person```

```python
from rest_framework import serializers

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "first", "last", "title"]
```

# Creating Views
You will need to create ```view```s to access resources, to modfiy them, to create them.

Below is how we create api view to get list of people.

You will use ```rest_framework.decorators.api_view``` and ```rest_framework.response.Response``` to create this view
This View returns response of list of people which are serialized as JSON objects
```python

@api_view(["GET"])
def list_people(request):
    people = Person.objects.all()
    serializer = PersonsSerializer(people, many=True)
    return Response({"people":serializer.data})
```

Then as it is usual, we will make url associate with this view within ```urls.py``` of people application

```python

from django.urls import path
from . import views

urlpatterns=[path("list_people/", views.list_people)]
```

And of course don't forget to include ```people``` application's ```urls``` within project's ```urls.py```

```python
from django.contrib import admin
from django.url import include,path

urlpatterns=[path("/admin",admin.site.urls),
             path("people/",include("people.urls"))]
```

# Viewsets

DRF components
- Serializers
  - Change objects into text and text back into objects
  - With or without the Djangon ORM
- Views
  - Utilities to write Django views that serialize and deserialize objects
- **ViewSets**
  - Class based view utilities encapsulating common REST/HTTP methods
- Router
  - Map between **ViewSet** and Django url routes

## ViewSet example from Docs
[Viewsets](docs/using_viewsets.md)

# Django Auth and DRF Permissions
[Django Auth and DRF Permissions](docs/djauth_and_permissions.md)

# Alternative Serializers
[Alternative Serializers](docs/alternative_serializers.md)