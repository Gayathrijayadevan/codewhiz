from django.urls import path
from . import views

urlpatterns=[
    path('',views.cw_login),
    path('register',views.register),
    path('u_home',views.u_home),
    path('a_home',views.a_home),
    path('quize',views.quize),

]