from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from .models import *
from django.contrib.auth.decorators import login_required
from Blog.forms import *
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from Blog.models import Post
from django.contrib.auth.models import User

# from django.shortcuts import render, get_object_or_404
# from django.views.generic.list import ListView
# from .models import *
# from django.contrib.auth.decorators import login_required
# from Blog.forms import *
# from django.http.response import HttpResponseRedirect
# from django.urls import reverse
# from django.template.context_processors import request
# from Blog.models import Post
# from django.contrib.auth.models import User

#제네릭뷰 : 장고에서 제공하는 여러가지 기능으로 나눈 뷰 클래스
#클래스 기반의 뷰
#class 뷰이름(기능별 뷰클래스):
#LiestView : 특정 객체의 ㅁ고록을 다루는 기능을 가진 뷰 클래스

class index(ListView):
    template_name = "Blog/templates/index.html"
    model = Post
    context_object_name = 'list'
    paginate_by = 5
    #template_name='' html파일 문자열을 넣음
    #model : 모델클래스명 입력
    #context_object_name : 템플릿에서 사용할 객체 리스트의 변수명
    #paginate_by : 한페이지에 몇개의 객체가 보일지 숫자를 입력
    
def detail(request, post_id):
    obj = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/templates/detail.html', { 'post' : obj })

@login_required
def posting(request):
    if request.method == "GET":
        form = PostForm
        return render(request, "blog/templates/posting.html", { "form" : form })
    elif request == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            #글쓴이를 저장하는 변수가 빈공간이므로 바로 데이터베이스 저장하지 않고 Post 객체로 변환
            obj = form.save(commit=False)
            obj.author = request.user   #요청한 클라이언트의 유저와 매칭
            obj.save()                  #객체를 데이터베이스 저장
            #request.FILES : 클라이언트가 보낸 파일들에 대한 데이터
            #Image 객체 생성 및 저장
            #HTML 폼에서 name이 images로 지정된 파일저장 input 태그
            for f in request.FILES.getlist('images'):
                image = Image(post=obj, image=f)#Image 객체 생성
                image.save()
            #File 객체 생성 및 저장
            for f in request.FILES.getlist('files'):
                file = File(post=obj, file=f)
                file.save()
                
            return HttpResponseRedirect( reverse('Blog:detail', args=(obj.id, )))      
        

def searchP(request):
    q = request.GET.get('q', '')
    type = request.GET.get('type', '0')
    #type : '0' 제목 검색
    if type == '0':
        #모델클래스.objects.filter() : 특정조건을 만족하는 모든객체 추출
        #filter, get, exclude에 조건을 넣을때 (모델 클래스의 변수 __명령어 = 값)
        #형태로 넣음
        list = Post.objects.filter(headline__contains=q)
        return render(request, "Blog/templates/searchP.html", { 'list' : list })
    #type : '1' 글쓴이 검색          
    if type == '1':
        user = User.objects.get(username__iexact = q)
        list = Post.objects.filter(author = user)
        return render(request, "Blog/templates/searchP.html", { 'list' : list })
