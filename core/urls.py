from django.urls import path
from . import views


urlpatterns = [
 
    path('', views.article_list, name='article_list'),  # Example view
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    #path('article/<int:pk>/', views.article_detail, name='article_detail'),  # Example detail view
    # Add more URL patterns for your views here


    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('therapist/', views.therapist_view, name='therapist'),
    path('therapistform/', views.therapistform_view, name='therapistform'),

    
]
