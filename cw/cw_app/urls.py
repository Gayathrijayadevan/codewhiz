from django.urls import path
from . import views

urlpatterns=[
    path('',views.cw_login),
    path('logout',views.cw_logout),
    path('register',views.register),
    path('a_home',views.a_home),
    path('quize', views.quize, name='quize'),    
    path('add_quize',views.add_quiz),
    path('edit_quize/<qid>',views.edit_quiz),
    path('del_quize/<qid>',views.delete_quiz),
    path('qns/<qid>',views.questions),
    path('add_qns',views.add_qns),

#--------------user-----------------------------
    path('u_home',views.u_home),

]