from django import forms

from .models import Question


class QuestionForm(forms.Form):
    question_text = forms.CharField(label="Question")
    pub_date = forms.DateTimeField(label="Date", widget=forms.SelectDateWidget)


class ChoiceForm(forms.Form):
    choice_text = forms.CharField(label="New choice")


class AdminChoiceForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    choice_text = forms.CharField(label="New choice")
    votes = forms.IntegerField(label="Initial votes number")
