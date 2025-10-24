from django.urls import path
from .views import health, ingest
urlpatterns=[path('ingest', ingest),
    path('health', health),
    ]
