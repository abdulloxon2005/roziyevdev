from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'course', 'amount', 'status', 'payment_method', 'paid_at', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'user__email', 'user__first_name', 'user__last_name', 'course__title', 'transaction_id')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    ordering = ('-created_at',)
