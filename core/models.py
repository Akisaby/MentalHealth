# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)

    # Add any other fields you need

    def __str__(self):
        return self.username

class Article(models.Model):
    DEPRESSION = 'Depression'
    ANXIETY = 'Anxiety'
    STRESS_MANAGEMENT = 'Stress Management'
    MINDFULNESS_MEDITATION = 'Mindfulness and Meditation'
    TRAUMATIC_DISORDER = 'Traumatic Disorder'

    CATEGORY_CHOICES = [
        (DEPRESSION, 'Depression'),
        (ANXIETY, 'Anxiety'),
        (STRESS_MANAGEMENT, 'Stress Management'),
        (MINDFULNESS_MEDITATION, 'Mindfulness and Meditation'),
        (TRAUMATIC_DISORDER, 'Traumatic Disorder'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='article_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=DEPRESSION)

    def __str__(self):
        return self.title

class Therapist(models.Model):
    profile_picture = models.ImageField(upload_to='therapists/')
    names = models.CharField(max_length=255)
    bio = models.TextField()
    telephone = models.CharField(max_length=15,help_text="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    email = models.EmailField()

    def __str__(self):
        return self.names



class Booking(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booking with {self.therapist.names} on {self.date}"
