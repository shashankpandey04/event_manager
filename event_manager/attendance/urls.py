from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.attendance_home, name='attendance_home'),
    path('attendance/<int:event_id>/', views.event_attendance, name='event_attendance'),
    path('attendance/<int:event_id>/scan/', views.scan_qr, name='scan_qr'),
    path('attendance/<int:event_id>/scan/process/', views.process_scan, name='process_scan'),
    path('attendance/<int:event_id>/checkin/<int:user_id>/', views.check_in, name='check_in'),
    path('attendance/<int:event_id>/checkout/<int:user_id>/', views.check_out, name='check_out'),
]
