from django.contrib import admin
from .models import Question, Survey, Choice, SurveyPage

admin.site.register(SurveyPage)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(Choice)
