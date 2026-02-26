from django.contrib import admin
from .models import CustomUser, PromptHistory, ChatHistory
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model



# over riding the default behaviour of Custom user model to looks cleaner interface
# in the admin panel

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(PromptHistory)

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'usermsg', 'display_msg')
admin.site.register(ChatHistory,ChatHistoryAdmin)