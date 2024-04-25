from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from event_track.models import MyClass

def send_class_cancel_notification():
    subject = 'Class Cancellation Notification'
    html_message = render_to_string('class_cancel_notification.html', {
        'class_name': MyClass.name,
        'class_date': MyClass.date,
        'class_time': MyClass.time
    })
    from_email = settings.EMAIL_HOST_USER
    receipent_list = MyClass.students.values_list('email', flat=True)
    send_mail(subject, html_message, from_email, receipent_list)