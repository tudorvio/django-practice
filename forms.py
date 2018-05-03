from django import forms
from .models import Choice, Question

#TODO: pass args, kwargs to constructor, pop fields, call super-constructor with args, kwargs, set self.fields
class SurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')

        super(SurveyForm, self).__init__(*args, **kwargs)

        for q in questions:
            choices = []
            for answer in q.choice_set.all():
                    choices.append((answer.pk, answer.choice_text))

            self.fields[q.id] = forms.ChoiceField(label=q.question_text, required=True, 
                                      choices=choices, widget=forms.RadioSelect)

    def answers(self):
        for q, a in self.cleaned_data.items():
            if not q.startswith('csr'):
                yield a
