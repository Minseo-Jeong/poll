from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from poll.models import Question, Choice

# Create your views here.

def index(request):
    # Question 테이블 객체를 pub_data 열의 역순으로 정렬하여 5개의 최근 객체를 리스트로 만듦.
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    # 템플릿에 넘겨주는 방식은 사전 타입. (템플릿에서 사용하는 변수명:해당 객체)
    context = {'latest_question_list':latest_question_list}
    # 랜더링, 템플릿 코드에 context 변수를 적용해서 최종 HTML 파일을 만들고 이를 담은 HttpResponse 객체를 반환.
    return render(request, 'poll/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html', {'question':question})
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'poll/detail.html', {
            'question':question,
            'error_message':"You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('poll:results', args=(question_id,)))    

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question':question})


