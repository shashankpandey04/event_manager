from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.view_events, name='view_events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
]
