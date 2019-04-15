from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email_application_enrollement(first_name, last_name, email):
    content = {
        'first_name': first_name,
        'last_name': last_name,
    }
    to_email = email
    subject = 'Student reprezentant'
    message = render_to_string('emails/email_application_enrollment.html', content)
    send_email = EmailMessage(subject, message, to=[to_email])
    send_email.send()
