from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic, View

from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm, AdminChoiceForm


class IndexView(View):

    def get(self, request):
        form = QuestionForm()
        latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        context = {
            'latest_question_list': latest_question_list,
            'form': form
        }
        return render(request, 'polls/index.html', context)

    def post(self, request):
        form = QuestionForm(request.POST)

        if form.is_valid():

            Question.objects.create(
                question_text=form.cleaned_data["question_text"],
                pub_date=form.cleaned_data["pub_date"]
            )

        else:
            messages.error(request, "Form was not valid")

        return HttpResponseRedirect(reverse('polls:index'))


class DetailView(View):

    def get(self, request, pk):
        # question = get_object_or_404(Question, pk=pk)
        choice_form = ChoiceForm()
        admin_choice_form = AdminChoiceForm()
        try:
            question = Question.objects.filter(pub_date__lte=timezone.now()).get(pk=pk)
            # question = Question.objects.all().get(pk=pk)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        context = {
            'question': question,
            'choice_form': choice_form,
            'admin_choice_form': admin_choice_form,
        }
        return render(request, 'polls/detail.html', context)

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        admin_form = False
        try:
            request.POST['votes']
            admin_form = True
        except KeyError:
            pass
        if admin_form:
            admin_choice_form = AdminChoiceForm(request.POST)
            if admin_choice_form.is_valid():
                Choice.objects.create(
                    question=admin_choice_form.cleaned_data["question"],
                    choice_text=admin_choice_form.cleaned_data["choice_text"],
                    votes=admin_choice_form.cleaned_data["votes"],
                )
        else:
            choice_form = ChoiceForm(request.POST)
            if choice_form.is_valid():
                Choice.objects.create(
                    question=question,
                    choice_text=choice_form.cleaned_data["choice_text"]
                )
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))


class EditView(View):

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = QuestionForm(
            initial={
                'question_text': question.question_text,
                'pub_date': question.pub_date
            }
        )
        context = {
            'question': question,
            'form': form
        }
        return render(request, 'polls/edit.html', context)

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question.question_text = form.cleaned_data["question_text"]
            question.pub_date = form.cleaned_data["pub_date"]
            question.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))


class ResultsView(View):

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        context = {
            'question': question,
        }
        return render(request, 'polls/results.html', context)


class VoteView(View):

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#         # 'test': True
#     }
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     choices = Choice.objects.filter(question=question_id)
#     context = {
#         'question': question,
#         'choices': choices
#     }
#     return render(request, 'polls/detail.html', context)
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'question': question,
#     }
#     return render(request, 'polls/results.html', context)
#
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#         # print("request.POST['choice']: ", request.POST['choice'])
#         # print("request.POST['każdy_inny_klucz_formularza']: ", request.POST['account_name'])
#         # print("request.POST: ", request.POST)
#         # print("selected_choice: ", selected_choice)
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# def detail(request, question_id, q_id, quest_id):
#     return HttpResponse("String {2}, par_2_from_endpoint: {1}, par_3: {0}".format(question_id, q_id, quest_id))

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         # raise Http404("Question does not exist")
#         question = None
#     questions = Question.objects.filter(pk=question_id)
#     question_value = None
#     for q in questions:
#         question_value = q
#         print(q.pub_date)
#     context = {
#         'question': question,
#         'questions': questions,
#         'question_value': question_value
#     }
#     return render(request, 'polls/detail.html', context)

# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         return Question.objects.order_by('-pub_date')[:5]
#
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'
