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
    pages = survey.surveypage_set.all().order_by('page_nr')
    attempt = Attempt.create(survey=survey)
    attempt.save()
    context = {'survey': survey, 'pages': pages, 'attempt': attempt}

    return render(request, 'survey/detail.html', context)

def step(request, survey_id, attempt_id, surveypage_nr):
    survey = get_object_or_404(Survey, pk=survey_id)
    attempt = get_object_or_404(Attempt, pk=attempt_id)
    pages = survey.surveypage_set.all().order_by('page_nr')
    page = pages.filter(page_nr=surveypage_nr).first();
    questions = page.question_set.all()

    rageHard = request.POST

    if request.method == 'POST':
        form = SurveyForm(request.POST)
    else:
        form = SurveyForm(questions=questions)

    print("it should be") 
    if request.method == 'POST':
        if form.is_valid():
            print("defo valid")
            attempt.score = 200
            qs = form.cleaned_data[fields]
            for field in qs:
                answer = get_object_or_404(field)
                attempt.score = attempt.score + 7 + answer.score
        attempt.score = attempt.score + 5
        attempt.save()
        print("HUEHUEHUEHEUHEUHEUHEUHEUHEUHUE")
        return HttpResponseRedirect(reverse('cucumber:results', args=(survey.id, attempt.id,)))
    
    else:        
        context = {'page': page, 'form': form}
        return render(request, 'survey/surveypage.html', context)

def results(request, survey_id, attempt_id):
    attempt = get_object_or_404(Attempt, pk=attempt_id)
    return render(request, 'survey/results.html', {'attempt': attempt})
