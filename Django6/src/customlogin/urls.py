from django.urls.conf import path
from .views import *
#인증(로그인, 로그아웃, 회원가입)에 관한 뷰가 있는 파일
from django.contrib.auth import views
app_name = 'customlogin'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', signin, name='signin'),
    #path('signin/', signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    ]