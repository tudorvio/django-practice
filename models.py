from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=70, default="Default Title")
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    passing_grade = models.IntegerField(default=10)

    def __str__(self):
        return self.title

class SurveyPage(models.Model):
    page_nr = models.IntegerField(null=True)       # UNIQUE TOGETHER
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True)

    def __str__(self):
        #return self.survey.title + " page " + self.id
        return "Page " + str(self.id)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    survey_page = models.ForeignKey(SurveyPage, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    score = models.IntegerField(null=True)

    def __str__(self):
        return self.choice_text


class Attempt(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    @classmethod
    def create(cls, survey):
        attempt = cls(survey=survey)
        return attempt

    def __str__(self):
        return "You scored: " + str(self.score)
