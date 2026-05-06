from django.urls import path
from . import views

urlpatterns = [
    path('registrations/', views.my_registrations_view, name='registrations'),
    path('registrations/<int:registration_id>/approve/', views.approve_registration, name='approve_registration'),
    path('registrations/<int:registration_id>/reject/', views.reject_registration, name='reject_registration'),
    path('register/<int:event_id>/', views.register_event_view, name='register_event'),
    path('unregister/<int:event_id>/', views.unregister_event_view, name='unregister_event'),
]
