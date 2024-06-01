from django.contrib import admin
from .models import Article
from django.contrib.auth.admin import UserAdmin
from .models import User,Therapist,Booking

admin.site.register(Therapist)
admin.site.register(User)
admin.site.register(Article)
admin.site.register(Booking)
