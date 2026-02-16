from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime

def send_welcome_mail(user):

    if not user.email:
        return

    context = {
        "user_name": user.fullName,
        "current_year": datetime.now().year,
        "dashboard_link": "http://127.0.0.1:8000/dashboard/",
    }

    html_content = render_to_string(
        "emails/welcome.html",
        context
    )

    email = EmailMultiAlternatives(
        subject="Welcome to Eventify — Your account is ready",
        body="Welcome to Eventify!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.attach_alternative(html_content, "text/html")

    email.send(fail_silently=False)
