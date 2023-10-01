from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Thumbnail, Plan, User, UserManager


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['username', 'plan']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # None is section title
        (
            ('Permissions'),  # title "permissions" passed to gettext_lazy
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'plan',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


admin.site.register(Thumbnail)
admin.site.register(Plan)
admin.site.register(User, UserAdmin)
