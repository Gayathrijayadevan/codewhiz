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
    path('qns/add_qns', views.add_qns, name='add_qns'),
    path('qns/edit_qns/<int:qid>/', views.edit_qns, name='edit_qns'),
    path('qns/del_qns/<int:qid>/', views.delete_qns, name='del_qns'),
    path('qns/<int:qid>/', views.questions, name='questions'),
    path('view_users',views.view_users),

#--------------user-----------------------------
    path('u_home',views.u_home),
    path('u_quiz', views.user_quizes, name='u_quiz'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('profile',views.profile),
    path('about',views.about),



]