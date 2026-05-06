from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/auth/login")
def admin_dashboard(request):
    if request.user.role not in ('organizer', 'admin'):
        return render(request, 'admin_panel/unauthorized.html')
    return render(request, 'admin_panel/dashboard.html')