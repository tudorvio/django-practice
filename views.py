from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Survey, SurveyPage, Choice, Attempt
from .forms import SurveyForm

def index(request):
    latest_survey_list = Survey.objects.order_by('-pub_date')[:5]
    context = {'latest_survey_list': latest_survey_list}
    return render(request, 'survey/index.html', context)

def survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    attempt = Attempt.create(survey=survey)
    attempt.save()
    context = {'survey': survey, 'attempt': attempt}

    return render(request, 'survey/detail.html', context)

def step(request, survey_id, attempt_id, surveypage_nr):
    survey = get_object_or_404(Survey, pk=survey_id)
    attempt = get_object_or_404(Attempt, pk=attempt_id)
    pages = survey.surveypage_set.all().order_by('page_nr')
    page = pages.filter(page_nr=surveypage_nr).first();
    questions = page.question_set.all()
    totalp = len(pages)

    # If it's the last page or not.
    if surveypage_nr == len(pages):
        next = 0
    else:
        next = surveypage_nr + 1

    form = SurveyForm(request.POST or None, questions=questions)

    if form.is_valid():
        for a in form.answers():
            answer = get_object_or_404(Choice, pk=a)
            attempt.score = attempt.score + answer.score
        attempt.save()
        if next == 0:
            return HttpResponseRedirect(reverse('results', args=(survey.id, attempt.id,)))
        else:
            return HttpResponseRedirect(reverse('step', args=(survey.id, attempt.id, next)))
    else:        
        context = {'page': page, 'form': form, 'next': next, 'totalp': totalp}
        return render(request, 'survey/surveypage.html', context)

def results(request, survey_id, attempt_id):
    attempt = get_object_or_404(Attempt, pk=attempt_id)
    return render(request, 'survey/results.html', {'attempt': attempt})
