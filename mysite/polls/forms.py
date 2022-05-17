from django import forms

from .models import Question, GENDER


class QuestionForm(forms.Form):
    question_text = forms.CharField(label="Question")
    pub_date = forms.DateTimeField(label="Date", widget=forms.SelectDateWidget)


class ChoiceForm(forms.Form):
    choice_text = forms.CharField(label="New choice")


class AdminChoiceForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    choice_text = forms.CharField(label="New choice")
    votes = forms.IntegerField(label="Initial votes number")


class PersonForm(forms.Form):
    name = forms.CharField(label="Name")
    surname = forms.CharField(label="Surname")
    gender = forms.ChoiceField(choices=GENDER)
    birth_date = forms.DateField(label="Birth date", required=False,
                                 widget=forms.SelectDateWidget(years=range(1980, 2022))
                                 )
    position = forms.CharField(label="Position", required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
