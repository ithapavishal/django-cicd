from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_approved')
    list_filter = ('role', 'is_approved')
    search_fields = ('user__username', 'user__email', 'role')

admin.site.register(Profile, ProfileAdmin)
