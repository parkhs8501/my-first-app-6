from django.db import models
from django.conf import settings
# Create your models here.
#글 종류 : PostType
class PostType(models.Model):
    name = models.CharField('구분', max_length=50)
    def __str__(self):
        return self.name
#글 : Post
#from django.conf import settings
class Post(models.Model):
    type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    headline = models.CharField('제목', max_length=200)
    #blank : 사용자가 입력 양식으로 입력할때 빈칸으로 둬도 되도록 허용
    #null : 데이터베이스에 저장할때 빈칸으로 둬도 되도록 허용
    content = models.TextField('내용', blank=True, null=True)
    #auth_now_add : 웹서버 기준의 현재 시간으로 자동 입력됨
    pub_date = models.DateField('날짜', auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#이미지, 파일을 저장, 관리하기 위해서 Django에서 'Pillow' 라이브러리를 사용
#글에 포함된 이미지 : Image
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #upload_to 변수 안에 %Y : 현재 년도,  %m : 현재 월, %d : 현재 일을 문자열에 넣어 객체가 생성된 시점에 따라 자동으로 분류해줌
    image = models.ImageField('이미지파일', upload_to='images/%Y/%m/%d')
    #ImageField는 이미지가 저장된 경로를 가지고 있어, 객체가 제거되도 실제 이미지
    #파일은 제거되지 않음, 때문에 delete함수를 오버라이딩해 해당 경로에 저장된 이미지를 지우는 행동이 필요함
    def delete(self, using=None, keep_parents=False):
        self.image.delete() #객체가 가지고 있는 이미지 경로에 있는 파일을 삭제
        return models.Model.delete(self, using=using, keep_parents=keep_parents)
#글에 포함된 파일 : File
class File(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField('파일', upload_to="files/%Y/%m/%d")
    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        return models.Model.delete(self, using=using, keep_parents=keep_parents)





