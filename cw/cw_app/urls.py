from django.urls import path
from . import views

urlpatterns=[
    path('',views.cw_login),
    path('logout',views.cw_logout),
    path('register',views.register),
    path('a_home',views.a_home),
    path('quize', views.quizze, name='quize'),    
    path('add_quize',views.add_quiz),
    path('edit_quize/<qid>',views.edit_quiz),
    path('del_quize/<qid>',views.delete_quiz),
    path('add_qns',views.add_qns),
    path('qns/edit_qns/<int:qid>/', views.edit_qns, name='edit_qns'),
    path('del_qns/<qid>',views.delete_qns),  
    path('qns/<int:qid>/', views.questions, name='questions'),

#--------------user-----------------------------
    path('u_home',views.u_home),
    path('u_quiz',views.user_quizes),



]