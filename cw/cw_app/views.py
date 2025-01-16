from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt


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

def a_home(req):
    total_quizzes = Quiz.objects.count()
    total_questions=Question.objects.count()
    cate=Category.objects.all()
    user=User.objects.exclude(last_login=None).count()
    attempts=QuizAttempt.objects.all()
    return render( req,'admin/a_home.html', {'c':cate,'quizes':total_quizzes,'qns':total_questions,'u':user,
                                             'attempts':attempts})   

def quizze(req):
    if 'admin' in req.session:
        search_query = req.GET.get('search', '')
        category_filter = req.GET.get('category', '')
        status_filter = req.GET.get('status', '')  
        
        if category_filter.isdigit():
            category_filter = int(category_filter)  
    
        quize = Quiz.objects.all()
        
        if search_query:
            quize = quize.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if category_filter:
            quize = quize.filter(category__id=category_filter)
            
        if status_filter:
            quize = quize.filter(status=status_filter)
            
        cate = Category.objects.all()
        
        difficulty_choices = [
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard')
        ]
        
        context = {
            'quiz': quize,
            'categ': cate,
            'search_query': search_query,
            'selected_category': category_filter,
            'selected_status': status_filter,
            'difficulty_choices': difficulty_choices
        }
    
        if req.headers.get('HX-Request'):
            return render(req, 'admin/partial_quize.html', context)   
        
        return render(req, 'admin/quize.html', context)
    else:
        return redirect(a_home)
    
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
            return redirect(quizze)
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
        return redirect(quizze)
    else:
        cate=Category.objects.all()
        data = Quiz.objects.get(pk=qid)
        return render(req, 'admin/edit_quiz.html', {'data': data,'cate':cate})
    
def delete_quiz(req,qid):
    data=Quiz.objects.get(pk=qid)
    data.delete()
    return redirect(quizze)    

def questions(req, qid):
    print(f"Incoming qid type: {type(qid)}, value: {qid}")
    qns = Question.objects.filter(quiz=qid)
    print(f"Questions found: {qns.count()}")
    for q in qns:
        print(f"Question {q.pk} for quiz {q.quiz.id}")
    return render(req, 'admin/questions.html', {'ques': qns})

def add_qns(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            quiz_id = req.POST.get('quiz')
            question_text = req.POST.get('question')
            option1 = req.POST.get('option1')
            option2 = req.POST.get('option2')
            option3 = req.POST.get('option3')
            option4 = req.POST.get('option4')
            points = req.POST.get('points')  
            correct_opt = req.POST.get('correct')
            quiz=Quiz.objects.get(pk=quiz_id)

            data = Question.objects.create(
                    quiz=quiz,
                    question_text=question_text,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    points=int(points),  
                    is_correct=correct_opt
                )
            return redirect(quizze)  
            
        else:
            quize = Quiz.objects.all()
            return render(req, 'admin/add_qns.html', {'qui': quize})
    else:
        return redirect(cw_login)  

def edit_qns(req,qid):
    if req.method == 'POST':
        quiz=req.POST['quiz']
        question_text = req.POST.get('question')
        option1=req.POST['option1']
        option2=req.POST['option2']
        option3=req.POST['option3']
        option4=req.POST['option4']
        point=req.POST['points']
        correct_opt=req.POST['correct'] 
        ques = Question.objects.get(pk=qid)

        ques. quiz=Quiz.objects.get(title=quiz)
        ques.question_text=question_text
        ques.option1=option1
        ques.option2=option2
        ques.option3 =option3
        ques.option4 =option4
        ques.points =point
        ques.is_correct=correct_opt

        ques.save() 
        return redirect(quizze) 
    else:
        quize = Quiz.objects.all()
        data = Question.objects.get(pk=qid)
        return render(req, 'admin/edit_questions.html', {'data': data,'qui': quize})

def delete_qns(req,qid):
    data=Question.objects.get(pk=qid)
    data.delete()
    return redirect(quizze)    

def view_users(req):
    user_data=User.objects.all()
    return render(req,'admin/view_users.html',{'users':user_data})
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

def u_home(req):
    data=Quiz.objects.all()[:3]
    categ_count=Category.objects.count()
    total_quizzes = Quiz.objects.count()
    categ=Category.objects.all()
    return render( req,'user/u_home.html',{'qdata':data,'cate':categ,'c_count':categ_count,'q_count':total_quizzes})

def user_quizes(req):
    if 'user' in req.session:
        search_query = req.GET.get('search', '')
        category_filter = req.GET.get('category', '')
        status_filter = req.GET.get('status', '')  
        
        if category_filter.isdigit():
            category_filter = int(category_filter)  
    
        quize = Quiz.objects.all()
        
        if search_query:
            quize = quize.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if category_filter:
            quize = quize.filter(category__id=category_filter)
            
        if status_filter:
            quize = quize.filter(status=status_filter)
            
        cate = Category.objects.all()
        
        difficulty_choices = [
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard')
        ]
        
        context = {
            'quiz': quize,
            'categ': cate,
            'search_query': search_query,
            'selected_category': category_filter,
            'selected_status': status_filter,
            'difficulty_choices': difficulty_choices
        }
    
        if req.headers.get('HX-Request'):
            return render(req, 'user/filter_result.html', context)   
        
        return render(req, 'user/quizzes.html', context)
    
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    attempt = QuizAttempt.objects.filter(
        user=request.user,
        quiz=quiz,
        completed=False
    ).first()
    
    if not attempt:
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            start_time=timezone.now()
        )
    
    questions = Question.objects.filter(quiz=quiz)
    
    elapsed_time = timezone.now() - attempt.start_time
    remaining_seconds = max(0, quiz.time_limit * 60 - elapsed_time.total_seconds())
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'attempt': attempt,
        'remaining_seconds': int(remaining_seconds)
    }
    
    return render(request, 'user/quize_dtl.html', context)

@login_required
@csrf_exempt
def submit_quiz(request, quiz_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'})
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = get_object_or_404(
        QuizAttempt, 
        user=request.user, 
        quiz=quiz, 
        completed=False
    )
    
    try:
        data = json.loads(request.body)
        answers = data.get('answers', {})
        
        score = 0
        total_points = 0
        
        # Process each answer
        for question in quiz.question_set.all():
            total_points += question.points
            selected_option = answers.get(str(question.id))
            
            if selected_option:
                # Get the actual text of the selected answer
                selected_text = getattr(question, selected_option, '')
                
                is_correct = selected_text == question.is_correct

                UserAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_choice=selected_text,
                    is_correct=is_correct
                )
                
                if is_correct:
                    score += question.points
        
        attempt.score = score
        attempt.completed = True
        attempt.end_time = timezone.now()
        attempt.save()
        
        percentage = (score / total_points * 100) if total_points > 0 else 0
        
        return JsonResponse({
            'score': score,
            'total_points': total_points,
            'percentage': round(percentage, 1)
        })
        
    except Exception as e:
        print(f"Error processing quiz submission: {str(e)}")  # Add logging
        return JsonResponse({'error': str(e)})
    
def profile(req) :
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        attempts=QuizAttempt.objects.filter(user=user)
        print(attempts)
        return render(req,'user/profile.html',{'user':user,'attempt':attempts})

def about(req):
    return render(req,'user/about.html')
