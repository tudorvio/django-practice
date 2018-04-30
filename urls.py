from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:survey_id>/', views.survey, name='survey'),
    path('<int:survey_id>/<int:attempt_id>/<int:surveypage_nr>', views.step, name='step'),
    path('<int:survey_id>/<int:attempt_id>/results>', views.results, name='results'),
]
