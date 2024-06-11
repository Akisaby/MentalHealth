from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from core.forms import FeedbackForm
from .models import Feedback, User, Therapist, Booking, Article

CATEGORIES = ['Depression', 'Anxiety', 'Stress Management', 'Mindfulness and Meditation', 'Traumatic Disorder']
def is_admin(user):
    return user.is_superuser

def is_therapist(user):
    return user.role == User.THERAPIST

def is_patient(user):
    return user.role == User.PATIENT

# Core views
def home(request):
    articles = Article.objects.all()
    therapists = Therapist.objects.all()
    return render(request, 'article/home.html',
     {'articles': articles, 'categories': CATEGORIES,'therapists': therapists,})


def therapist_list(request):
    therapists = Therapist.objects.all()
    return render(request, 'therapist/therapist_list.html', {'therapists': therapists, 'categories': CATEGORIES})

def therapist_detail(request, therapist_id):
    therapist = get_object_or_404(Therapist, pk=therapist_id)
    return render(request, 'therapist/therapist_detail.html', {'therapist': therapist, 'categories': CATEGORIES})

@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback-confirm')
    else:
        form = FeedbackForm()
    return render(request, 'article/feedback.html', {'form': form})

def feed_confirm(request):
    return render(request, 'article/feedback_confirm.html')

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

        return redirect('booking_confirmation')

    return render(request, 'therapist/booking.html', {'therapist': therapist, 'categories': CATEGORIES})

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
        confirm_password = request.POST['confirm_password']
        telephone = request.POST['telephone']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
                try:
                    user = User.objects.create_user(full_name=full_name, email=email, username=username, password=password, telephone=telephone)
                    auth_login(request, user)
                    return redirect('login')
                except Exception as e:
                    messages.error(request, str(e))

    return render(request, 'registration/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.role == User.THERAPIST:
                return redirect('therapist_dashboard')
            else:
                # Assume other users are patients or unspecified roles
                return redirect('patient_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html')

def custom_logout(request):
    auth_logout(request)
    return redirect('login')

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article/article_list.html', {'articles': articles, 'categories': CATEGORIES})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article/article_detail.html', {'article': article, 'categories': CATEGORIES})

def category_list(request):
    return render(request, 'article/category_list.html', {'categories': CATEGORIES})

def article_by_category(request, category_name):
    articles = Article.objects.filter(category=category_name)
    return render(request, 'article/article_by_category.html', {'articles': articles, 'categories': CATEGORIES, 'category_name': category_name})

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

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Count therapists
    num_therapists = Therapist.objects.count()
    num_feeback = Feedback.objects.count()
    # Count patients
    num_patients = User.objects.filter(role=User.PATIENT).count()
    # Count articles
    num_articles = Article.objects.count()
    # Count bookings
    num_bookings = Booking.objects.count()
    context = {
        'total_feedback' : num_feeback,
        'total_therapists': num_therapists,
        'total_patients': num_patients,
        'total_articles': num_articles,
        'total_bookings': num_bookings,
    }
    return render(request, 'admin-dash/admin_dashboard.html',context )

@login_required
@user_passes_test(is_therapist)
def therapist_dashboard(request):
    num_therapists = Therapist.objects.count()
    num_feeback = Feedback.objects.count()
    # Count patients
    num_patients = User.objects.filter(role=User.PATIENT).count()
    # Count articles
    num_articles = Article.objects.count()
    # Count bookings
    num_bookings = Booking.objects.count()
    context = {
        'total_feedback' : num_feeback,
        'total_therapists': num_therapists,
        'total_patients': num_patients,
        'total_articles': num_articles,
        'total_bookings': num_bookings,
    }
    return render(request, 'therapist-dash/therapist_dashboard.html',context)

def bookings_list(request):
    bookings = Booking.objects.filter(therapist=request.user.therapist)  # Assuming therapist is linked to the request user
    return render(request, 'therapist-dash/bookings.html', {'bookings': bookings})

def view_bookings(request):
    bookings = Booking.objects.filter(therapist=request.user.therapist)  # Assuming therapist is linked to the request user
    return render(request, 'therapist-dash/view_bookings.html', {'bookings': bookings})

def confirm_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    # Add logic to confirm booking (e.g., update status)
    return redirect('view_bookings')

def reject_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    # Add logic to reject booking (e.g., update status)
    return redirect('view_bookings')

@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    my_bookings = Booking.objects.count()
    return render(request, 'patient-dash/patient_dashboard.html',{'bookings': bookings, 'my_bookings':my_bookings})

from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('article_list')  # Redirect to article list page
    else:
        form = ArticleForm()
    return render(request, 'therapist-dash/add_article.html', {'form': form})
