# Am I restricted to serialize Django Models?

- No. You are not restricted to Django database ORM objects
- Use the base ```serializers.Serializer``` class combined with serializer fields to construct arbitrary objects
- Creating serializer fields is similar to how you declare a model ORM object.

# Show me

We will use a new app called ```vehicles```

```bash
python manage.py startapp vehicles
```

- As usual add ```vehicles``` app into ```INSTALLED_APPS``` list within ```settings.py``` file of the project
- Create ```urls.py``` and define ```urlpatterns``` list to contain the app urls

For this examples we will have no Django model ORMs.

Within ```vehicles/models/tools.py``` we will define ```Tool``` object

```python
class Tool:
    def __init__(self, name, make):
        self.name = name
        self.make = make
```

To be able to import ```Tool``` object directly from ```models```, we will import it inside ```__init__.py``` file
of ```models``` directory.

Now, within ```vehicles/serializers/tools.py```

```python
from rest_framework import serializers


class ToolSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    make = serializers.CharField(max_length=50)
```

Notice that instead of ```ModelSerializer``` we are using ```Serializer```
We are defining a field for each of the corresponding fields of ```Tool``` object.

Next we will creat a view that will serialize a list of tool objects and return them as response.

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Tool
from serializers import ToolSeriaizer


@api_view(["GET"])
def list_tools(request):
    tools = [Tool("knife", "Ikea"), Tool("wrench", "Cargo")]
    serializer = ToolSeriaizer(tools, many=True)
    content = {"tools": serializer.data}
    return Response(content)
```

And to make our views accessible we will define a path associated with it

````python
from django.urls import path
from views import tools

urlpatterns = [path("list_tools/", tools.list_tools)]
````

# Many Serializer fields
Most are String fields, what changes is validation

- BooleanField
- CharField
- EmailField
- RegexField
- SlugField
- URLField
- UUIDField
- FilePathField
- IPAddressField

**Numeric**
- IntegerField
- FloatField
- DecimalField

**Data and Time**
- DateTimeField
- DateField
- TimeField
- DurationField

**Choice/Selection**
- ChoiceField
- MultipleChoiceField

**Field*
Fields for uploaded files
- FileField
- ImageField

**Composite**
Fields that are collections
- ListField
- DictField
- HStoreField
- JSONField

**Others**
SerializerMethodField maps to a method inside a Serializer. This allows you to run arbitrary code when serializing data.

- ReadOnlyField
- HiddenField
- ModelField
- SerializerMethodField

# Serializer field arguments
When instantiating you can use arguments to control behavior.

Common serializer field arguments:
- read_only
- write_only
- required
- default
- allow_null
- **source** : by default Serializer uses the name of the fields to look up corresponding object field. If you need to rename object field or get data from some other source, you can use this field to specify the **source** of the field
- validators : just like django model validators to determine the values of the object field are valid
- error_messages
- label
- help_text
- initial
- style : to specify the presentation. depending on Renderer can be useful

Look up **serializers fields** documentation https://www.django-rest-framework.org/api-guide/fields

