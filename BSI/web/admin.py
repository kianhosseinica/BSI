from django.contrib import admin
from .models import CostEstimate, UserProfile

class CostEstimateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'method', 'website_type', 'traffic', 'maintenance', 'created_at')
    list_filter = ('method', 'website_type', 'maintenance', 'created_at', 'user')
    search_fields = ('website_type', 'method', 'user__username')

admin.site.register(CostEstimate, CostEstimateAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'first_name', 'last_name', 'email', 'email_verified')
    search_fields = ('user__username', 'phone', 'first_name', 'last_name', 'email')
    list_filter = ('email_verified',)

admin.site.register(UserProfile, UserProfileAdmin)
