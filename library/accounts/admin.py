from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    pass
    model = CustomUser
    list_display = ["username",]