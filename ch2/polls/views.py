from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from polls.models import Choice, Question

# Create your views here.

def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list':latest_question_list} #템플릿에 넘겨주는 방식은 사전 타입
    return render(request, 'polls/index.html', context)
    # render() 함수는 polls/index.html에 context 변수를 적용하여 최종 HTML 텍스트를 만들고 이를 담아서 HttpResponse 객체를 반환

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id) #이 함수의 첫 번째 인자는 모델 클래스이고 두 번째 인자부터는 검색 조건
    return render(request, 'polls/detail.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 설문 투표 폼을 다시 보여준다.
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':"You didn't select a choice.",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # POST 데이터를 정상적으로 처리했으면
        # 항상 HttpResponseRedirect를 반환하여 리다이렉션 처리함
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
    
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})