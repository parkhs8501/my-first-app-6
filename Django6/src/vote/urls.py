from django.urls import path
from .views import *
#{% url 'vote:index' %}
app_name = 'vote'
urlpatterns = [
    path('', index, name='index'),
    path('<int:question_id>/', detail, name='detail'),
    path('vote/<int:question_id>/',vote, name='vote'),
    path('result/<int:question_id>/', result, name='result'),
    path('registerQ/', registerQ, name='registerQ'),
    path('deleteQ/<int:question_id>/', deleteQ, name='deleteQ'),
    path('registerC/<int:question_id>/', registerC, name='registerC'),
    path('deleteC/<int:choice_id>/', deleteC, name="deleteC"),
    path('updateQ/<int:question_id>/', updateQ, name="updateQ"),
]
