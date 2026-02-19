from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    if request.user.role != 'organizer':
        return render(request, 'admin/unauthorized.html')
    return render(request, 'admin/dashboard.html')