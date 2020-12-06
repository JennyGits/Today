from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from bs4 import BeautifulSoup

from polls.models import Question, Choice


def main(request):
    return render(request, 'polls/main.html')

# def index(request):
#     return HttpResponse('hello')


def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     return HttpResponse("you are looking at question %s"% question_id)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # choice = get_object_or_404(Choice, pk=choice_id)
    # choice = get_object_or_404(Choice, pk=choice_id)
    return render(request, 'polls/detail.html', {'question': question});

# def results(request, question_id):
#     return HttpResponse("results of question %s" %question_id)

#global cho_id
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    votes = []
    for cho in question.choice_set.all():
        votes.append(cho.votes)
        #result = {cho: cho.votes}
        # for i in cho.votes[i]:
        #     if(i >= 1):
    print(votes)

    # votes[0] 하면 첫번째 vote 숫자값 들어있음
    return render(request, 'polls/results.html', {'question': question})

# def vote(request, question_id):
#     return HttpResponse("you are voting on question %s"% question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    cho_id = request.POST.get('choice')
    choice = get_object_or_404(Choice, pk=cho_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', kwargs={'question_id': question.id}))

