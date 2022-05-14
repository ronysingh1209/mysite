from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Contact, Course
from django.conf import settings
from django.contrib import auth
from django.views import View


# def home(request):
#     # print(dir(request))
    
#     # print(request.session.get('password'))
    
#     # return HttpResponse("<h1 style='text-align:center;'>Home Page</h1>")

#     context = {
#         'alert_msg': 'Home Page',
#         'title': 'Home'
#     }

#     return render(request, "myapp/index.html", context)


class Home(View):
    def get(self, request):
        context = {
            'alert_msg': 'Home Page',
            'title': 'Home'
        }

        return render(request, "myapp/index.html", context)


# @cache_page(60)
def about(request):
    # return HttpResponse("<h1 style='text-align:center;'>About Page</h1>")

    context = {
        'alert_msg': 'About Page',
        'title': 'About'
    }

    return render(request, "myapp/about.html", context)


def contact(request):
    if request.method == 'GET':
        # return HttpResponse("<h1 style='text-align:center;'>Contact Page</h1>")

        context = {
            'alert_msg': 'Contact Page',
            'title': 'Contact'
        }

        return render(request, "myapp/contact.html", context)
    
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        Contact(name=name, email=email, message=message).save()
        
        # return HttpResponse("<h1 style='text-align:center;'>Thank you for contacting us!</h1>")
        
        return redirect('/')


def dashboard(request):
    context = {
        'alert_msg': 'Dashboard',
        'title': 'Dashboard',
    }

    return render(request, 'myapp/dashboard.html', context=context)


@staff_member_required
@login_required
def add_course(request):
    if request.method == 'GET':
        context = {
            'alert_msg': 'Add Courses Page',
            'title': 'Add Courses',
        }
        
        return render(request, "myapp/addCourse.html", context)
    
    else:
        title = request.POST.get('title')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.POST.get('image')
        
        # return HttpResponse(f"{title}\n{price}\n{description}\n{image}")
        
        Course(title=title, description=description, image=image, price=price).save()
        
        return redirect('/')


@login_required
def courses(request):
    # return HttpResponse("<h1 style='text-align:center;'>Course Page</h1>")
    
    context = {
        'alert_msg': 'Courses Page',
        'title': 'Courses',
        'courses': Course.objects.values(),
    }

    return render(request, "myapp/courses.html", context)


@login_required
def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        
        if search != "":
            allCourses = Course.objects.filter(title__icontains=search)
        
        else:
            allCourses = []
        
        # return HttpResponse(f"<h1 style='text-align:center;'>{search}</h1>")
        
        context = {
            'alert_msg': f'Search For : {search.title()}',
            'title': 'Search',
            'allCourses': list(allCourses),
        }
        
        return render(request, 'myapp/search.html', context)


@login_required
def courseDetailsByID(request, courseID):
    if request.method == 'GET':
        course = Course.objects.get(id=courseID)
        
        # return HttpResponse(f"<h1 style='text-align:center;'>Course ID - {courseID}</h1>")
        
        context = {
            'alert_msg': f'Course ID : {courseID}',
            'title': 'Course Details',
            'course': course,
        }
        
        return render(request, "myapp/courseDetailsByID.html", context)


@login_required
def courseDetailsByName(request, courseName):
    # return HttpResponse(f"<h1 style='text-align:center;'>Course Name - {courseName}</h1>")
    
    context = {
        'alert_msg': f'Course Name : {courseName.title()}',
        'title': 'Course Details',
    }
    
    return render(request, "myapp/courseDetailsByName.html", context)


@login_required
def course_api(request):
    courses = Course.objects.values('id', 'title', 'description', 'price', 'image')

    context = {
        'courses': list(courses),
    }

    return JsonResponse(context)


def register(request):
    if request.method == "GET":
        context = {
            'alert_msg': 'Register Page',
            'title': 'Register'
        }
        
        return render(request, "myapp/register.html", context)
    
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # print(f"Name : {username}\nEmail : {email}\nPassword : {password}")
        
        user = User.objects.get(username=username)
        
        if not user:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        
        else:
            return redirect('/login')
        
        subject = 'WELCOME TO OUR COMPANY APPWARS TECHNOLOGIES'
        message = f'Hi, Thank you for registering in Appwars Technologies.\nHave a nice journey!\n\nAnshul Garg\n(Data Scientist)'
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        
        send_mail(subject, message, email_from, recipient_list)
        
        # return HttpResponse(f"<h1 style='text-align:center;'>You are now registered!</h1>")
        
        return redirect('/login')


def login(request):
    if request.method == 'GET':
        context = {
            'alert_msg': 'Login Page',
            'title': 'Login'
        }
        
        return render(request, "myapp/login.html", context)

    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        request.session.set_expiry(60 * 60 * 24)
        request.session['password'] = password
        
        # print(f"Username : {username}\nPassword : {password}")
        
        user = auth.authenticate(username=username, password=password)
        
        if user is None:
            # return HttpResponse(f"<h1 style='text-align:center;'>You are not verified!</h1>")
            
            return redirect('/')
        
        else:
            auth.login(request, user)
            # return HttpResponse(f"<h1 style='text-align:center;'>You are now logged in!</h1>")
        
            return redirect('/courses')


def logout(request):
    auth.logout(request)
    
    # return redirect('/')
    # return HttpResponse(f"<h1 style='text-align:center;'>You are now logged out!</h1>")
    
    context = {
        'alert_msg': 'You are now logged out!',
        'title': 'Logout'
    }
    
    return render(request, "myapp/logout.html", context)
