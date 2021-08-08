from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from users.models import User

# class UserAdminConfig(UserAdmin):
#     search_fields = ('email',)
#     list_filter = ('email',)
#     ordering = ('-updated_at',)
#     list_display = ('email', 'is_active', 'is_verified', 'is_staff', 'created_at', 'updated_at',)
#     fieldsets = (
#         (None, {'fields': ('email',)}),
#         ('Permissions', {'fields': ('is_staff', 'is_verified', 'is_active',)}),
#     )

admin.site.register(User)
