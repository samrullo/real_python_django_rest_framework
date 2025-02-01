# Compounded serializers
So far we showed how to create ViewSets for a single django db model object.
There can be cases where from your Single Page Applications you want to pull data related to multiple object types.

- A common pattern is to declare API that includes multiple objects
- Everthing you might need in a single-page-application
- Declare a view and nest multiple serializers

# We will use new app
We will create new django app called ```api```

```bash
python manage.py startapp api
```

As usual add new app into INSTALLED_APPS, create new urls.py

# First compound viewsets

Here is our first compound viewset

```python
from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from Fedora.artifacts.models import Artifact
from Fedora.people.models import Person
from Fedora.vehicles.models import Vehicle
from Fedora.people.serializers import PersonSerializer
from Fedora.vehicles.serializers import VehicleSerializer


@api_view(["GET"])
def listing(request):
    doctors = Person.objects.filter(title="Dr.")
    vehicles = Vehicle.objects.all()

    context = {"request": request}
    vehicle_serializer = VehicleSerializer(vehicles, many=True, context=context)

    results = {"doctors": PersonSerializer(doctors, many=True).data,
               "vehicles": vehicle_serializer.data}
    return Response(results)
```

Notice how we passed ```context``` when initializing ```VehicleSerializer```. 
This is because ModelSerializer needs request object to construct ```url``` field.
```serializers.ModelViewSet``` takes care of this automatically, 
but when we use VehicleSerializer with url field in isolation we have to context dictionary with request object.

# Define urls
We define urls

```python
from django.urls import path, include
from . import views

urlpatterns = [path("v1/listing/", views.listing)]
```

Notice how we specified url with v1 prefix specifying the api version.
This is a good practice when you have to update your api.
This way your users can still access oder versions while you work on newer versions of your api.

# Without the Router
- if you are not using ```ViewSets``` and ```Routers```, you don't get the benefit of having your view listed in the root path.
- What if I wanted it? You can write a ```ViewSet``` that does the same thing as any view.

Below is a new ViewSet we added to our ```api.views```

```python
class DoctorsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    def list(self, request):
        doctors = Person.objects.filter(title="Dr.")
        results = {"doctors": PersonSerializer(doctors, many=True).data}
        return Response(results)

```

```DoctorsViewSet``` inherits from two classes, ```GenericViewSet``` because it is a viewset.
- Next it inherits from ```mixinx.ListModelMixin``` which tells what HTTP methods this viewset will support. ListModelMixin tells that DoctorsViewSet will only support listing.

Now I can declare a router and register my newly defined viewset above into it

```python
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r"doctors", DoctorViewSet,"doctor")

urlpatterns=[path("v1/", include(router.urls)),
             path("v1/listing/", views.listing)]
```

With that when I hit api/v1 it will give me possible sub-urls that I can use.


# ViewSet classes
- ViewSet
- GenericViewSet : which adds ```queryset```, ```get_object()``` and ```get_queryset()``` methods
- ModelViewSet
- ReadOnlyModelViewSet : also a ModelViewSet but doesn't allow changes

Base ```ViewSet``` implements 6 methods that correspond to REST API actions such as GET, POST, PUT, PATCH, DELETE

```python
class UserViewSet(viewsets.ViewSet):
    def list(self,request):
        pass
    def create(self,request):
        pass
    def retrieve(self, request, pk=None):
        pass
    def update(self, request, pk=None):
        pass
    def partial_update(self, request, pk=None):
        pass
    def destroy(self, request, pk=None):
        pass
```

# Viewsets Mixins
Each of above methods are declared inside of a **Mixin**.
So that you can **mix** and **match** the Mixins and create ViewSets that only support methods that you want to allow.

- mixins.CreateModelMixin
- mixins.ListModelMixin
- mixins.RetrieveModelMixin
- mixins.UpdateModelMixin : provides both ```update``` and ```partial_update``` methods
- mixins.DestroyModelMixin

Essentially there is a **Mixin** for every method of REST API.

# Additional actions
- Declare your own views/routes by adding an **action**
- Decorate a method of ```ViewSet``` subclass
- Common usage : mass operations
  - REST by default doesn't allow deletion of multiple objects at once. You have to make separate calls to delete every object.
  - As a workaround you can create an action called mass_delete

Below is how we write code to mass delete artifacts

```python
class MassDeleteArtifactsViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    @action(detail=False, methods=["delete"])
    def mass_delete(self, request, pk=None):
        for artifact_id in request.POST["ids"].split(","):
            Artifact.objects.get(id=artifact_id).delete()

        return Response({"message":f"mass deletion of {request.POST['ids']} completed"})
```

- detail=False tells url to access this method won't include an id
- next we are passing a list of HTTP methods allowed for the action
- We are passing list of ids as a text in POST request

You will have to register the newly created viewset to the router.

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"doctors", views.DoctorsViewSet, "doctor")
router.register(r"mass_delete", views.MassDeleteArtifactsViewSet, "mass_delete")

urlpatterns = [path("v1/", include(router.urls)),
               path("v1/listing/", views.listing)]

```

Now let's run curl to mass delete artifacts

```bash
$ curl -X DELETE -d "ids=4,5,6" http://127.0.0.1:8000/api/v1/mass_delete/mass_delete/
```

one gotcha, mass_delete doesn't appear as accessable REST routes when I hit api/v1 root

