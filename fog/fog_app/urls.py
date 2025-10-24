from django.urls import path
from .views import health, upload
urlpatterns=[path('upload', upload),
    path('health', health),
    ]
