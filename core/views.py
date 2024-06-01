from django.conf import settings
from django.shortcuts import render, get_object_or_404,redirect
from .models import Article
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import User
# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Therapist, Booking
from django.utils import timezone

def therapist_list(request):
    therapists = Therapist.objects.all()
    return render(request, 'therapist/therapist_list.html', {'therapists': therapists})

def therapist_detail(request, therapist_id):
    therapist = get_object_or_404(Therapist, pk=therapist_id)
    return render(request, 'therapist/therapist_detail.html', {'therapist': therapist})

@login_required
def book_therapist(request, therapist_id):
    therapist = get_object_or_404(Therapist, pk=therapist_id)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        age = request.POST['age']
        category = request.POST['category']
        date = request.POST['date']
        message = request.POST['message']

        # Send email to the therapist
        send_mail(
            'New Appointment Booking',
            f'You have a new appointment booking from {first_name} {last_name}.\n\n'
            f'Phone Number: {phone_number}\n'
            f'Age: {age}\n'
            f'Category: {category}\n'
            f'Preferred Date: {date}\n\n'
            f'Message:\n{message}',
            settings.DEFAULT_FROM_EMAIL,
            [therapist.email],
            fail_silently=False,
        )

        # Redirect to a success page
        return redirect('booking_confirmation')

    return render(request, 'therapist/booking.html', {'therapist': therapist})

def booking_confirmation(request):
    return render(request, 'therapist/booking_confirmation.html')
















def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "registration/password_reset_email.txt"
                c = {
                    "email": user.email,
                    'domain': request.get_host(),
                    'site_name': 'Your Site',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email_content = render_to_string(email_template_name, c)
                send_mail(subject, email_content, 'admin@yourdomain.com', [user.email], fail_silently=False)
        return redirect('password_reset_done')
    return render(request, 'registration/password_reset.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = "/login/"


def register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        telephone = request.POST['telephone']

        user = User.objects.create_user(full_name=full_name, email=email, username=username, password=password, telephone=telephone)
        auth_login(request, user)  # Use auth_login to avoid conflict with the view name
        return redirect('login')  # Redirect to your home page
    return render(request, 'registration/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use auth_login to avoid conflict with the view name
            return redirect('therapist')  # Redirect to your home page
        else:
            # Handle invalid login
            return render(request, 'registration/login.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'registration/login.html')

def custom_logout(request):
    auth_logout(request)  # Use auth_logout to avoid conflict with the view name
    return redirect('login')


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article/article_list.html',{'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    articles = Article.objects.all()
    context ={'articles': articles,'article': article}
    return render(request, 'article/article_detail.html',context)

def pricing_view(request):
    return render(request, 'pricing.html')


def therapist_view(request):
    return render(request, 'therapist.html')

def therapistform_view(request):
    return render(request, 'therapistform.html')

def passrecovery_view(request):
    return render(request, 'passrecovery.html')

def about_view(request):
    return render(request, 'about.html')