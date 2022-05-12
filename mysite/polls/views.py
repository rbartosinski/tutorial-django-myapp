from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, question_id):
    return HttpResponse("String %s" % question_id)
    # return HttpResponse("String {0}".format(question_id))


def results(request, question_id):
    return HttpResponse("String results %s" % question_id)


def vote(request, question_id):
    return HttpResponse("String vote %s" % question_id)
