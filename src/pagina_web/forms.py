from django import forms

from pagina_web.models import ApplicationEnrollment, FrequentlyAskedQuestions


class ApplicationEnrollmentForm(forms.ModelForm):
    class Meta:
        model = ApplicationEnrollment
        fields = ["first_name", "last_name", "email", "birth_date", "country", 'county', "city", "nationality",
                  "study_type", "faculty", "specialization", "year_of_study", "motivation"]

    def __init__(self, *args, **kwargs):
        super(ApplicationEnrollmentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class FrequentlyAskedQuestionsForm(forms.ModelForm):
    class Meta:
        model = FrequentlyAskedQuestions
        fields = ["question", "answer"]

    def __init__(self, *args, **kwargs):
        super(FrequentlyAskedQuestionsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
