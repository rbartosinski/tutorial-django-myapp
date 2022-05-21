from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser, User, Group
from django.db.models import Count
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic, View

from .models import Question, Choice, Person
from .forms import QuestionForm, ChoiceForm, AdminChoiceForm, PersonForm, LoginForm, RegistrationForm, \
    QuestionSearchForm


class IndexView(View):

    def get(self, request):
        form = QuestionForm()
        # latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        # latest_question_list = Question.objects.all().exclude(question_text="Moje nowe pytanie")
        # latest_question_list = Question.objects.order_by("question_text") # .all().order_by()
        # latest_question_list = Question.objects.order_by("question_text")[:1] # .all().order_by()
        # latest_question_list = Question.objects.order_by('pub_date').distinct('pub_date')
        # latest_question_list = Question.objects.filter(question_text__startswith="jakie")
        # latest_question_list = Question.objects.filter(id__lte=5)
        latest_question_list = Question.objects.filter(question_text__contains="pytanie").filter(id__gte=5)
        latest_question = Question.objects.latest('id')
        print(latest_question.question_text)
        # for i in latest_question_list:
        #     print(i.question_text)
        #     print(i.pub_date)
        #     print(i.pk) # == i.id
        context = {
            'latest_question_list': latest_question_list,
            'form': form,
        }
        if not request.user.is_anonymous:
            persons = Person.objects.all()
            context["persons"] = persons
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


class QuestionSearchView(View):

    def get(self, request):
        form = QuestionSearchForm()
        context = {
            'form': form
        }
        return render(request, 'polls/search.html', context)

    def post(self, request):
        form = QuestionSearchForm(request.POST)
        results = None
        if form.is_valid():

            if form.cleaned_data["question_text"] != '':
                results = Question.objects.filter(
                    question_text__contains=form.cleaned_data["question_text"]
                )
            else:
                pass

            if not results:
                if form.cleaned_data["pub_date"] != '':
                    results = Question.objects.filter(
                        pub_date=form.cleaned_data["pub_date"]
                    )
            else:
                if form.cleaned_data["pub_date"] != '':
                    results = Question.objects.filter(
                        question_text__contains=form.cleaned_data["question_text"]
                    ).filter(
                        pub_date=form.cleaned_data["pub_date"]
                    )
        context = {
            'form': form,
            'results': results
        }
        return render(request, 'polls/search.html', context)


class DetailView(LoginRequiredMixin, View):

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
        choice_form = ChoiceForm(request.POST)
        if choice_form.is_valid():
            Choice.objects.create(
                question=question,
                choice_text=choice_form.cleaned_data["choice_text"]
            )
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))


class EditView(PermissionRequiredMixin, View):
    permission_required = 'polls.change_question'
    raise_exception = True

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


class ResultsView(PermissionRequiredMixin, View):
    permission_required = 'polls.change_question'
    raise_exception = True

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        context = {
            'question': question,
        }
        return render(request, 'polls/results.html', context)


class VoteView(PermissionRequiredMixin, View):
    permission_required = 'polls.change_question'
    raise_exception = True

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


class DeleteView(PermissionRequiredMixin, View):
    permission_required = 'polls.change_question'
    raise_exception = True

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return HttpResponseRedirect(reverse('polls:index'))


class AdminChoiceView(PermissionRequiredMixin, View):
    permission_required = 'polls.change_choice'
    raise_exception = True

    def get(self, request):
        form = AdminChoiceForm()
        context = {
            "admin_choice_form": form
        }
        return render(request, 'polls/admin_choice.html', context)

    def post(self, request):
        admin_choice_form = AdminChoiceForm(request.POST)
        if admin_choice_form.is_valid():
            Choice.objects.create(
                question=admin_choice_form.cleaned_data["question"],
                choice_text=admin_choice_form.cleaned_data["choice_text"],
                votes=admin_choice_form.cleaned_data["votes"],
            )
        else:
            messages.error(request, "Form was not valid")
        return HttpResponseRedirect(reverse('polls:index'))


class AddPerson(PermissionRequiredMixin, View):
    permission_required = 'polls.change_question'
    raise_exception = True

    def get(self, request):
        form = PersonForm()
        context = {
            "form": form
        }
        return render(request, 'polls/add_person.html', context)

    def post(self, request):
        form = PersonForm(request.POST)
        if form.is_valid():
            Person.objects.get_or_create(
                name=form.cleaned_data["name"],
                surname=form.cleaned_data["surname"],
                gender=form.cleaned_data["gender"],
                birth_date=form.cleaned_data["birth_date"],
                position=form.cleaned_data["position"],
                description=form.cleaned_data["description"],
            )
        else:
            messages.error(request, "Form was not valid")
        return HttpResponseRedirect(reverse('polls:index'))


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                url = request.GET.get('next')
                if url:
                    return redirect(url)

                return HttpResponseRedirect(reverse('polls:index'))

            messages.error(request, "Username or password invalid")
            return HttpResponseRedirect(reverse('polls:login'))

        messages.error(request, "Form was not valid")
        return HttpResponseRedirect(reverse('polls:login'))


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('polls:login'))


class RegistrationView(View):

    def get(self, request):
        form = RegistrationForm()
        context = {
            "form": form
        }
        return render(request, 'register.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] == form.cleaned_data["password_conf"]:
                try:
                    User.objects.get(username=form.cleaned_data["username"])
                    messages.error(request, "User already exists")
                    return HttpResponseRedirect(reverse("polls:registration"))
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        username=form.cleaned_data["username"],
                        password=form.cleaned_data["password"],
                        email=form.cleaned_data["email"]
                    )
                    group = Group.objects.get(name='standard')
                    user.groups.add(group)
                    login(request, user)
                    return HttpResponseRedirect(reverse("polls:index"))
            else:
                messages.error(request, "Passwords are wrong!")
                return HttpResponseRedirect(reverse("polls:registration"))


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
