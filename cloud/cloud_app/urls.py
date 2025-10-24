from django.urls import path
from .views import process, health
urlpatterns=[path('process', process),
    path('health', health),
    ]
