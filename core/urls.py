from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Example view
    path('articles', views.article_list, name='article_list'),  # Example view
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/categories/', views.category_list, name='category_list'),
    path('category/<str:category_name>/', views.article_by_category, name='article_by_category'),
    path('feedback/',views.feedback, name='feedback'),
    path('feedback-confirm/',views.feed_confirm, name='feedback-confirm'),


    path('therapists/', views.therapist_list, name='therapist_list'),
    path('therapists/<int:therapist_id>/', views.therapist_detail, name='therapist_detail'),
    path('therapists/<int:therapist_id>/book/', views.book_therapist, name='book_therapist'),
    path('booking/confirmation/', views.booking_confirmation, name='booking_confirmation'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('pricing/', views.pricing_view, name='pricing'),
    # path('therapist/', views.therapist_view, name='therapist'),
    path('therapistform/', views.therapistform_view, name='therapistform'),
    path('passrecovery/', views.passrecovery_view, name='passrecovery'),
    path('about/', views.about_view, name='about'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('therapist-dashboard/', views.therapist_dashboard, name='therapist_dashboard'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('add_article/', views.add_article, name='add_article'),

    path('bookings_list/', views.bookings_list, name='bookings_list'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    path('bookings/<int:booking_id>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('bookings/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
]
