from django import forms
from .models import Choice, Question

#TODO: pass args, kwargs to constructor, pop fields, call super-constructor with args, kwargs, set self.fields
class SurveyForm(forms.Form):
    def __init__(self, questions):
        super(SurveyForm, self).__init__()
        if questions != None:
            for q in questions:
                #if not isinstance(q, str):
                choices = []
                for answer in q.choice_set.all():
                    choices.append((answer.pk, answer.choice_text))

                self.fields[q] = forms.ChoiceField(label=q.question_text, required=True, 
                                      choices=choices, widget=forms.RadioSelect)
