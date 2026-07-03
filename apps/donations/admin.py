from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('guest', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('guest__full_name', 'guest__email', 'mercadopago_payment_id')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
