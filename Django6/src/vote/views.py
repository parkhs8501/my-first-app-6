from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
#reverse(문자열, args=튜플)
#문자열에 해당하는 url 별칭을 찾고, 매개변수가 필요한 URL일 경우
#args 매개변수에 있는 튜플값으로 자동 매핑

from .models import Question, Choice
from django.http.response import HttpResponseRedirect

import datetime #파이썬 내장모듈, 시간정보를 얻을 때 사용

from .form import *
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from vote.form import QuestionForm
#from . import w
#from . import forms #froms.QuestionForm

#view.py : 내부적으로 동작할 행동들을 정의
#HTML 파일 전달, 검색, 등록, 삭제, 수정
#함수 or 클래스 형태로 뷰 구현
#함수 형태로 구현시 반드시 첫번째 매개변수로 request 사용
#request : 웹 클라이언트의 요청에 대한 정보를 담고 있는 변수
def index(request):
    print("index 함수 호출")
    #Question.objects.all : Question 모델 클래스에 모든 객체 추출
    list = Question.objects.all()
    #render(request, html 파일경로, 템플릿에 전달할 데이터-사진형)
    #return render(request, "templates/index.html", {'question_list' : list})
    return render(request, "vote/templates/index.html", {'question_list' : list})

def detail(request, question_id):
    #get_object_or_404 : 모델클래스에 id값으로 객체 1개를 반환하는 함수
    #만약 객체를 못찾는 경우 클라이언트에게 404에러 메시지를 전달
    p = get_object_or_404(Question, pk = question_id)
    return render(request, "vote/templates/detail.html", {'question' : p})

def vote(request, question_id):
    #request.method : 클라이언트의 요청 방식이 저장된 변수
    #"GET", "POST" 문자열 비교. 대소문자 구분
    if request.method == "POST":
        #request.POST : POST 반식으로 들어온 데이터들
        #request.POST.get(문자열) : POST 방시그로 들어온 데이터 중 name 속성의 값이 문자열과 같은 데이터를 추출
        #get 함수가 반환하는 데이터는 무조건 문자열
        #input radio의 name
        id = request.POST.get('choice')
        obj = get_object_or_404(Choice, pk = id)
        obj.votes += 1
        obj.save() #모델클래스의 객체.save() : 변동사항을 저장
        #튜플을 만들때 요소 개수가 한개면 사칙연산에 사용하는 우선순위 괄호로 판단함. 때문에 튜플 요소 개수가 한개일 경우 끝에 쉼표를 입력
        #return HttpResponseRedirect(reverse('result', args=(question_id, )))
        return HttpResponseRedirect(reverse('vote:result', args=(question_id, )))
        #redirect(문자열) : 문자열에 해당하는 Url 주소로 변경
        #return redirect('/result/%s/' % (question_id))
    
def result(request, question_id):
    #모델클래스.objects.get(조건) : 조건에 맞는 객체를 1개 찾아 반환
    data = Question.objects.get(id = question_id)
    return render(request, "vote/templates/result.html", {'obj' : data})

@login_required
def registerQ(request):
    if request.method == "GET":
        form = QuestionForm() #QuestionForm 객체생성, 사용하는 속성들이 공란
        
        return render(request, "vote/templates/registerQ.html", {'form' : form})        
    elif request.method == "POST":
        form = QuestionForm(request.POST)
        
        #폼객체.is_valid() : 해당 폼에 입력값들이 에러가 ㅇ벗는지 확인
        #True, False 값 반환, 폼 객체 사용시 반드시 사용해야되는 함수
        if form.is_valid():
            #폼객체.save() : 해당 폼에 입력값들로 모델클래스 객체를 데이터베이스에 저장
            #데이터베이스에 저장후 반환
            #폼객체.save(commit=False) : 데이터베이스에 바로 저장하지 않고 모델폼에서 모델클래스 객체로 변환 후 반환
            obj = form.save(commit=False)
            #name = request.POST.get('question_text')
            #obj = Question()
            #obj.question_text = name
            #request.user.get_username() : 로그인된 회원의 username을 반환하는 함수
            user = User.objects.get(username=request.user.get_username())
            obj.pub_date = datetime.datetime.now()
            obj.author=user
            obj.save()
            return HttpResponseRedirect(reverse('vote:detail', args=(obj.id, )))
        else: #입력 양식에 문자가 있을 경우의 처리
            #템플릿으로 form 전달하면 사용자가 이전에 작성한 내용이 들어있는 상태로 전달함
            return render(request, "vote/templates/registerQ.html", {'form' : form, 'error' : "입력이 잘못됬습니다."})
               
@login_required            
def deleteQ(request, question_id):
    #pk = id
    obj = get_object_or_404(Question, pk = question_id)
    if obj.author.username != request.user.get_username():
        return render(request, "vote/templates/error.html", {'error' : '잘못된 접근 입니다.', 'returnURL' : reverse('vote:detail',
                                                                                                             args=(question_id, ))})
    obj.delete() #해당 객체를 데이터베이스에서 삭제
    return HttpResponseRedirect(reverse('vote:index'))  
  
@login_required 
def deleteC(request, choice_id):
    obj = get_object_or_404(Choice, pk = choice_id)
    if request.user.get_username() != obj.question.author.username:
        return render(request, "vote/templates/error.html", {'error' : '잘못된 접근 입니다.', 'returnURL' : reverse('vote:detail',
                                                                                                             args=(obj.question.id, ))})
    
    id = obj.question.id #choice 객체 삭제전에 Question 객체의 id값 저장
    obj.delete() #해당 객체를 데이터베이스에서 삭제
    return HttpResponseRedirect(reverse('vote:detail', args=(id, ))) 
    #return HttpResponseRedirect(reverse('vote:index'))  

def registerC(request, question_id):
    obj = get_object_or_404(Question, pk = question_id)
    #obj.author    해당 Quetion 객체를 작성한 User 객체
    #해당 질문을 쓴 글쓴이 이름과 로그인된 유저의 이름을 비교
    if request.user.get_username() != obj.author.username:
        return render(request, "vote/templates/error.html", {'error' : '본인이 작성한 글이 아닙니다.', 'returnURL' : reverse('vote:detail',
                                                                                                                  args=(question_id, ))})
    if request.method == "GET":
        #폼 객체 생성
        #render함수로 HTML파일 로드
        form = ChoiceForm()
        return render(request, "vote/templates/registerC.html", {'form' : form, 'name' : obj.question_text}) 
    elif request.method == "POST":            
        form = ChoiceForm(request.POST)
        
        if form.is_valid():
            obj1 = form.save(commit=False) #모델클래스 객체를 데이터베이스에 저장 및 반환
            obj1.question = obj
            obj1.save()
            return HttpResponseRedirect(reverse('vote:detail', args=(obj1.question.id, )))
        else:
            return render(request, "vote/templates/registerC.html", {'form' : form, 'error' : "입력이 잘못됬습니다.", 'name' : obj.question_text })

#뷰 함수 정의 시 위에 @함수명을 작성하면, 해당 뷰를 호출하기 전에 함수명에 해당하는 함수가 먼저 호출되 처리됨        
@login_required
def updateQ(request, question_id):
    obj = get_object_or_404(Question, pk = question_id)
    #obj.author    해당 Quetion 객체를 작성한 User 객체
    #해당 질문을 쓴 글쓴이 이름과 로그인된 유저의 이름을 비교
    if request.user.get_username() != obj.author.username:
        return render(request, "vote/templates/error.html", {'error' : '본인이 작성한 글이 아닙니다.', 'returnURL' : reverse('vote:detail',
                                                                                                                  args=(question_id, ))})
    if request.method == "GET":
        #Question 객체에 저장된 값을 QuestionForm 객체를 생성할 때 입력
        #모델폼의 생성자에 instance 매개변수는 이미 생성된 모델클래스의 객체를 담을 수 있음
        form = QuestionForm(instance = obj)
        return render(request, "vote/templates/updateQ.html", {'form' : form})
    elif request.method == "POST":
        #이미 생성된 Question 객체에 내용을 클라이언트가 작성한 내용으로 덮어씌움
        form = QuestionForm(request.POST, instance=obj)
        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = datetime.datetime.now()
            question.save()    
            return HttpResponseRedirect(reverse('vote:detail', args=(question.id, )))
        else:
            return render(request, "vote/templates/updateQ.html", {'form' : form, 'error' : "유효하지 않은 데이터"})
            
        