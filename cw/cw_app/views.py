from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def cw_login(req):
        if 'admin' in req.session:
            return redirect(a_home)
        if 'user' in req.session:
            return redirect(u_home)
        if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            data=authenticate(username=uname,password=password)
            if data:
                login(req,data)
                if data.is_superuser:
                    req.session['admin']=uname 
                    return redirect(a_home)
                else:
                    req.session['user']=uname 
                    return redirect(u_home)
            else:
                messages.warning(req,'invalid username or password')
                return redirect(cw_login)  
        else:
            return render(req,'login.html')
def cw_logout(req):
    logout(req)
    req.session.flush() 
    return redirect(cw_login)        
    
def u_home(req):
    return render( req,'user/u_home.html')

def quize(req):
    if 'admin' in req.session:
        quize=Quiz.objects.all()
        return render( req,'admin/quize.html',{'quiz':quize})
    
def add_quiz(req):
    if 'admin' in req.session:
        if req.method=='POST':
            title=req.POST['title']
            cate=req.POST['category']
            des=req.POST['descrip']
            time=req.POST['time']
            stat=req.POST['status']
            cat=Category.objects.get(pk=cate)
            data=Quiz.objects.create(title=title,category=cat,description=des,time_limit=time,status=stat)
            data.save()
            return redirect(quize)
        else:
            cate=Category.objects.all()
            return render(req,'admin/add_quiz.html',{'cate':cate})
        
    else:
        return redirect(cw_login)  

def edit_quiz(req,qid):
    if req.method == 'POST':
        title=req.POST['title']
        cate=req.POST['category']
        des=req.POST['descrip']
        time=req.POST['time']
        stat=req.POST['status']  
        quiz = Quiz.objects.get(pk=qid)

        quiz.title=title
        quiz. category =Category.objects.get(name=cate)
        quiz.description=des
        quiz.time_limit=time
        quiz.status =stat

        quiz.save()
        return redirect(quize)
    else:
        cate=Category.objects.all()
        data = Quiz.objects.get(pk=qid)
        return render(req, 'admin/edit_quiz.html', {'data': data,'cate':cate})

def questions(req):
    qns=Question.objects.all()
    return render(req,'admin/questions.html',{'ques':qns})

#-------------------------user---------------------
def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['password']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswd)
            data.save()
        except:
            messages.warning(req,'invalid username or password')
            return redirect(register)   
        return redirect(cw_login) 
    else:
        return render(req,'user/register.html') 

def a_home(req):
    return render( req,'admin/a_home.html')
        


