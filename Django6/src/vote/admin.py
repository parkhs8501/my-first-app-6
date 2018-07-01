#admin.py : 관리자사이트에서 모델클래스를 조회, 삽입, 삭제, 수정
#하고자 할때 설정하는 파이썬 파일

from django.contrib import admin
#해당 파일에서 모델클래스를 알아야되므로 from ~ import 를 사용
from .models import Question, Choice #from .models import *
#관리자 페이지에서 효과적으로 객체정보를 볼수있는 ModelAdmin클래스 상속
class ChoiceAdmin(admin.ModelAdmin):
    fields = ['choice_text', 'votes', 'question']
    list_display = ('choice_text', 'votes', 'question')
#admin.site.register(클래스명)
#해당 모델클래스를 관리자사이트 등록

# Register your models here.

#Question 모델클래스를 관리자사이트에서 접근할수 있도록 설정
admin.site.register(Question) 
#Choice 모델클래스를 관리자사이트에서 접근할수 있도록 설정
admin.site.register(Choice) 