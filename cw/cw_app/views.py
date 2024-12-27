from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
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
    
def u_home(req):
    return render( req,'user/u_home.html')

def quize(req):
    return render( req,'admin/quize.html')