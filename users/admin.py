from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import CustomUser


# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ['id', 'email', 'display_name']

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'bio', 'display_name']
    ordering = ('email',)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", 'is_staff', 'is_active'),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
