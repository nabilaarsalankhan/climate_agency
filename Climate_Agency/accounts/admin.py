from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "country", "is_staff", "is_active")
    search_fields = ("username", "email", "country")
    ordering = ("username",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "country")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "country", "password1", "password2", "is_staff", "is_active")}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
