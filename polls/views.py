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
    global last_result
    last_result = 0
    result = 0
    i = 0
    for cho in question.choice_set.all():
        votes.append(cho.votes)
        #a = votes.index(1)
        for i in range(0,votes[i]):
            if (votes[i] >= 1):
                if(i == 0):
                    result += 1
                else:
                    result -= 1
            else:
                print('투표 안 함')
            i += 1
        # if (a is None):
        #     print('votes를 리셋하세요')
        # if (a == 0):
        #     result += 1
        # if (a == 1):
        #     result -= 1
        last_result += result
    print('choice id : ', cho.id)
    print('votes 값: ', votes)
    #print('choice 인덱스: ', i)
    print('result: ', result)
    print(last_result)

    # votes[0] 하면 첫번째 vote 숫자값 들어있음
    return render(request, 'polls/results.html', {'question': question})

def last_result_page(request):
    global last_result
    if (last_result>=2):
        return render(request, 'polls/last_result_happy.html')
    if (last_result <=0):
        return render(request,'polls/last_result_bad.html')


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

