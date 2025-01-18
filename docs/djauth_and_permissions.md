# How to govern access to REST APIs
DRF allows us to restrict access to resources with ```rest_framwork.permissions```

When defining ```ModelViewSet``` we can pass to ```permission_classes``` 
things like ```IsAuthenticate```, ```IsAdmin``` or define custom permissions by extending ```BasePermission``` 
and overriding ```has_permission``` or ```has_object_permission``` methods.

## Django Authentication very quick
Before that we have to define at least the login page.

So we will make ```templates/registration/login.html``` right under project folder.
```login.html``` will be a simple form like below

```html
<body>

<div class="login-container">
    <h2>Login</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Login</button>
    </form>

    {% if form.errors %}
        <div class="error">Invalid username or password. Please try again.</div>
    {% endif %}
</div>

</body>
```

We will include ```django.contrib.auth.urls``` within project ```urls.py```

```python
urlpatterns=[path("accounts/", "django.contrib.auth.urls"),...]
```

We will specify templates folder within ```settings.py``` 

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

And we will specify ```LOGIN_REDIRECT_URL``` and ```LOGOUT_REDIRECT_URL``` too.

```python
LOGIN_REDIRECT_URL = "/books/library/"
LOGOUT_REDIRECT_URL = "/books/library/"
```

# Books app to demonstrate DRF Permissions
We will create couple of users from django admin page, one that is a staff and one that isn't.
Then we will make django app called books.
As usual we will create ```Book``` model and ```BookSerializer```.
And ```BookViewSet``` but with permissions

```python
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from .serializers import BookSerializer
from .models import Book
from django.contrib.auth.decorators import login_required


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsSuperUser | IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Book.objects.all()
        return Book.objects.filter(restricted=False).all()


@login_required
def library(request):
    return render(request, "library.html")
```
