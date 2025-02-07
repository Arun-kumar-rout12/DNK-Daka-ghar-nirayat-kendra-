from django.contrib import admin
from .models import UserProfile, UserPost, person, AgentProfile,Receipt

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

class UserPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date')
    search_fields = ('user__username', 'post')
    list_filter = ('date',)

class ShipmentBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'pickup_date', 'payment_method', 'date_created', 'status', 'payment_status')
    search_fields = ('name', 'contact_number', 'from_address', 'to_address', 'current_address')
    list_filter = ('pickup_date', 'payment_method', 'date_created')
    list_editable = ('status', 'payment_status')

class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('agent_id', 'name', 'phone_number')
    search_fields = ('agent_id', 'name', 'phone_number')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserPost, UserPostAdmin)
admin.site.register(person, ShipmentBookingAdmin)
admin.site.register(AgentProfile, AgentProfileAdmin)
