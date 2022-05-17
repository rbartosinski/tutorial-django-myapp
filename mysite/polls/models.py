import datetime

from django.db import models
from django.utils import timezone


GENDER = (
    (1, "Female"),
    (2, "Male")
)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Person(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=250)
    gender = models.IntegerField(choices=GENDER)
    birth_date = models.DateField(null=True)
    position = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
