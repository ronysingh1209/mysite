# from django.views.decorators.cache import cache_page
from django.urls import path
# from myapp import views
from . import views

urlpatterns = [
    # path('', views.home, name="home"),
    path('', views.Home.as_view(), name="home"),
    path('about/', views.about, name="about"),
    # path('about/', cache_page(60)(views.about), name="about"),
    path('contact/', views.contact, name="contact"),
    path('courses/', views.courses, name="courses"),
    path('courses/<int:courseID>', views.courseDetailsByID, name="courseDetailsByID"),
    path('courses/<str:courseName>', views.courseDetailsByName, name="courseDetailsByName"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('search/', views.search, name="search"),
    path('add_course/', views.add_course, name="add_course"),
    path('course_api/', views.course_api, name="course_api"),
    path('dashboard/', views.dashboard, name="dashboard"),
]