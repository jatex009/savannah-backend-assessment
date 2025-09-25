from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_verified', 'date_joined')
    list_filter = ('is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone_number')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Customer Info', {
            'fields': ('phone_number', 'address', 'date_of_birth', 'is_verified')
        }),
    )
