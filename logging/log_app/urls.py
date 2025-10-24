from django.urls import path
from .views import log_entry, get_logs, health
urlpatterns=[path('log', log_entry),
    path('logs', get_logs),
    path('health', health),
    ]
