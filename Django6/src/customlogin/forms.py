from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput

class UserForm(ModelForm):
    #모델클래스와 유사하게 변수에 XXField 객체르 ㄹ만들어 입력양식에 들어갈 <input>태그를 만들 수 있음
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())
    class Meta:
        #django에서 자동으로 생성된 사용자 모델클래스
        model = User
        #widgets : 각 속성의 입력 스타일을 설정
        #키 : 속성명
        #값 : forms.위젯클래스()
        widgets={
            'password' : forms.PasswordInput(),
            'email' : forms.EmailInput() 
            }
        fields = ['username', 'email', 'password']
        
        
class LoginForm(ModelForm):
    class Meta:
        model = User
        widgets={
            'password' : forms.PasswordInput()
            }
        fields=['username', 'password']
            
        