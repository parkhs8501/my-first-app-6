#form : HTML코드에서 사용할 입력양식을 모델클래스에 맞게 자동으로 만들어주는 기능 or 커스텀 입력양식을 만드는 기능을 제공함
#class 폼클래스명(ModelForm) : 모델클래스에 관한 폼을 정의
#class 폼클래스명(Form) : HTML에서 사용할 커스텀 폼을 정의
#class 폼클래스명(Form) : HTML에서 사용할 커스텀 폼을 정의
from django.forms.models import ModelForm
from . import models

class QuestionForm(ModelForm):
    class Meta: #Meta클래스 정의를 통해 모델 클래스에 관한 정보 입력
        #model : 모델클래스 명
        #fields or exclude
        #fields : 해당 모델폼을 통해 클라이언트가 입력할 수 있는 데이터 종류를 작성
        #exclude : 모델 클래스의 속성중 명시한 속성을 제외한 속성들을 사용자 작성
        model = models.Question
        fields = ['question_text']
        #exclude = ['pub_date'] #pub_date 속성을 제외한 모든 속성들을 사용자가 작성

#choice에 대한 모델폼 정의
#choice_text, question
#모델 폼을 만들때, 모델 클래스를 참고하면서 제작
class ChoiceForm(ModelForm):
    class Meta:
        model = models.Choice
        fields = ['choice_text']     
        #exclude = ['votes']   