"""
URL patterns for the core app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events_page, name='events'),
    path('admissions/', views.admissions_page, name='admissions'),
    path('academics/', views.academics_page, name='academics'),
    path('campus-life/', views.campus_life_page, name='campus_life'),
    path('student-corner/', views.student_corner_page, name='student_corner'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
]
