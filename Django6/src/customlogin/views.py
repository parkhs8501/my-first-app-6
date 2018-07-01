from django.shortcuts import render
from .forms import *
from django.contrib.auth import login, authenticate
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
# Create your views here.
def signup(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, "customlogin/templates/signup.html", {'form' : form})
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            #form.cleaned_data : 폼객체에 저장된 값들을 꺼낼때 사용(딕셔너리,사전형)
            #def func1(q, b, **a) **a : q, b 매개변수 외에 다른 값들이 들어오면 사전형으로 a 변수가 처리
            #create_user(username=form.cleand_data['username'],
            #            password=form.cleand_data[email],
            #            email=form.cleand_data['username'])
            #create_user(username, password, email) : 장고에서 지원하는 User 모델 클래스에 새로운 객체를 만들때 사용
            #모델클래스에 새로운 객체를 만들때 사용
            #패스워드 확인
            if form.cleaned_data['password'] == form.cleaned_data['password_check']:              
                #new_user = User.objects.create_user(**form.cleaned_data)
                new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                                    form.cleaned_data['password'])
                #login(request, User 객체) : 해당요청을 보낸 클라이언트가 User 객체로 로그인하는 작업을 함
                login(request, new_user)
                return HttpResponseRedirect(reverse('vote:index'))
            else:
                error = "비밀번호가 맞지않음"
        else:
            error = "유효하지 않은 값이 입력됨" 
        return render(request, "customlogin/templates/signup.html", {'form' : form , 'error' : error})      
    
    
def signin(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "customlogin/templates/signin.html", {'form' : form})
    elif request.method == "POST":
        form = LoginForm(request.POST) #ID, 비밀번호 실패시 보낼 폼
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        #authenticate(username, password) : User 모델클래스에 해당 ID와 Password로 저장된 객체를 찾아 반환 객체가 없는 경우 None 반환
        user = authenticate(username=username1, password=password1)
         # (값,변수) is 타입 : (값, 변수)가 타입과 동일한지 Ture, False 반환
         #user is not None == not( user is None )
        if user is not None: #user 변수의 값이 None 탕비이 아닌가?
            login(request, user) #로그인
            return HttpResponseRedirect(reverse("vote:index"))
        else: #해당 ID와 비밀번호를 가진 User 객체가 없는 경우
             error = "아이디 또는 비밀번호가 틀렸습니다."
        #else:
        #    error="유요하지 않은 데이터 입니다."
        return render(request, "customlogin/templates/signin.html", {'form' : form , 'error' : error})
                        
    #else