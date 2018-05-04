from django import forms
from .models import Choice, Question

class SurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')

        super(SurveyForm, self).__init__(*args, **kwargs)

        for q in questions:
            choices = []
            for answer in q.choice_set.all():
                    choices.append((answer.pk, answer.choice_text))

            self.fields[str(q.id)] = forms.ChoiceField(label=q.question_text, required=False, 
                                      choices=choices, widget=forms.RadioSelect)

    def answers(self):
        for q, a in self.cleaned_data.items():
            yield a
