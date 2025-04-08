from django.contrib import admin
from .models import User



class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "username", "role", "is_staff", "is_active", "created_at"]
    list_filter = ["role", "is_staff", "is_active"]
    search_fields = ["email", "username"]
    ordering = ["created_at"]
    readonly_fields = ["id", "created_at"]

admin.site.register(User, UserAdmin)