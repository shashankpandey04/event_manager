from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.view_events, name='view_events')
]
