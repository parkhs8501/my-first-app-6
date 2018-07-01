from django.forms.models import ModelForm
from .models import Post, Image, File

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('pub_date', 'author')
        
    def __init__(self, *args, **kwargs):    
        super(PostForm, self).__init__(*args, **kwargs)
        #사용자가 글 종류를 선택하지 않았을 때의 기본값
        self.fields['type'].empty_label = None

# class ImageForm(ModelForm):
#     class Meta:
#         model = Image
#         fields = ('images', )