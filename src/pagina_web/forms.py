from django import forms

from pagina_web.models import ApplicationEnrollment


class ApplicationEnrollmentForm(forms.ModelForm):
    class Meta:
        model = ApplicationEnrollment
        fields = ["first_name", "last_name", "email", "birth_date", "study_type", "faculty", "specialization",
                  "year_of_study", "motivation"]
