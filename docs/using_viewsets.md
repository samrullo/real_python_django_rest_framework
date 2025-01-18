## ViewSet example from Docs

```python
class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        maps to GET to get all resources
        """
        pass
    
    def create(self, request):
        """
        maps to POST to create a resource
        """
        pass
    def retrieve(self,request, pk=None):
        """
        maps to GET top get a specific resource
        """
        pass
    def update(self, request, pk=None):
        """
        maps to PUT to update a resource
        """
        pass
    def partial_update(self, request, pk=None):
        """
        maps to PATCH to update certain attributes of the resource
        """
        pass
    def destroy(self, request, pk=None):
        """
        maps to HTTP method DELETE to delete a resource
        """
        pass
```

# We will build new apps artifacts

- Add another app
  ```bash 
    python manage.py startapp artifacts
  ```

- Edit Fedora/settings.py, adding ```artifacts``` to ```INSTALLED_APPS```
- Edit Fedora/urls.py including ```artifacts.urls``` in the ```url_patterns``` list
- Follow along with ```models.py```, ```serializers.py```, ```views.py``` and ```urls.py``` as shown 
- Create an ```admin.py``` file for the models if desired
- Run ```makemigrations``` and ```migrate``` as needed
- User the ```admin``` or the ```loaddata``` command to add some data

# Artifacts viewsets
As before we will create a model Artifact that has only two fields name and shiny
We will make serializers and create ArtifactSerializer and associate it with model Artifact

And we will create viewsets
All we need is to specify the serializer and queryset to the viewsets and DRF will take care of everything else.

```python
from rest_framework import viewsets

from .models import Artifact
from .serializers import ArtifactSerializer

class ArtifactViewset(viewsets.ModelViewSet):
    serializer_class = ArtifactSerializer
    
    def get_queryset(self):
        return Artifact.objects.all()
```

# Using router to generate urls for the viewset
Within ```urls.py``` of artifacts app we will leverage ```rest_framework.routers``` to generate all urls to get, create and update artifacts.

```python

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"artifacts", views.ArtifactViewset, "artifact")

urlpatterns = [path("", include(router.urls))]

```

# Use curl to get, create and update artifacts

```bash
curl -s http://localhost:8000/artifacts | python -m json.tool
```

To create a new artifact
```bash
curl -s -X POST -d "name=Arc of the Covenants" -d "shiny=True" http://localhost:8000/artifacts/ | python -m json.tool
```

To update an artifact
```bash
curl -s -X PUT -d "name=Golden Idol" -d "shiny=True" http://localhost:8000/artifacts/1/ | python -m json.tool
```

to update one attribute
```bash
$ curl -s -X PATCH -d "shiny=False" http://localhost:8000/artifacts/1/ | python -m json.tool
```

to delete
```bash
$ curl -s -X DELETE http://localhost:8000/artifacts/2/
```


# Summary
By specifying ViewSet you automatically get the REST methods
  - List, Retrieve, Create, Update, Update Partial, and Delete
