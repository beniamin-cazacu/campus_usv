from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from pagina_web.models import User


def send_email_application_enrollement(student_id, first_name, last_name, email, domain):
    """ Function for send email to each applicant
            @:param student_id - student id
            @:param first_name, last_name, email - applicant details
            @:param domain -  website domain
            """
    content = {
        'student_id': student_id,
        'first_name': first_name,
        'last_name': last_name,
        'domain': domain
    }
    to_email = email
    subject = 'Student reprezentant'
    message = render_to_string('emails/email_application_enrollment.html', content)
    send_email = EmailMessage(subject, message, to=[to_email])
    send_email.send()


def register_new_student(student, domain):
    """
      Function for registering the student after he / she has been accepted
      :param student: student object
      :param domain: website domain
      """

    generate_password = BaseUserManager().make_random_password(length=6)
    new_student = User()
    new_student.first_name = student.first_name
    new_student.last_name = student.last_name
    new_student.email = student.email
    new_student.set_password(generate_password)
    new_student.save()
    save_profile(new_student.pk, student)

    # send email
    to_email = student.email
    subject = 'Student reprezentat'
    content = {
        'first_name': student.first_name,
        'last_name': student.last_name,
        'domain': domain,
        'email': student.email,
        'password': generate_password
    }
    message = render_to_string('emails/email_applicant_accepted.html', content)
    send_email = EmailMessage(subject, message, to=[to_email])
    send_email.send()


def student_rejected(student, domain):
    """
    the rejected student will receive an email
    :param student:
    :param domain:
    """
    to_email = student.email
    subject = 'Student reprezentat'
    content = {
        'first_name': student.first_name,
        'last_name': student.last_name,
        'domain': domain,
    }

    message = render_to_string('emails/email_applicant_rejected.html', content)
    send_email = EmailMessage(subject, message, to=[to_email])
    send_email.send()


def save_profile(user, student):
    """
    Create an account for the accepted student
    :param user: new user account
    :param student: student object
    """
    user = User.objects.get(pk=user)
    user.profile.avatar = student.avatar
    user.profile.birth_date = student.birth_date
    user.profile.study_type = student.study_type
    user.profile.country = student.country
    user.profile.county = student.county
    user.profile.city = student.city
    user.profile.nationality = student.nationality
    user.profile.faculty = student.faculty
    user.profile.specialization = student.specialization
    user.profile.year_of_study = student.year_of_study
    user.save()
