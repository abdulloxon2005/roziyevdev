from django.urls import path
from .views import (
    web_checkout_view,
    web_process_payment_view,
    web_order_success_view,
)

urlpatterns = [
    # Web sahifalar
    path('checkout/<slug:slug>/', web_checkout_view, name='order_checkout'),
    path('pay/<str:order_number>/', web_process_payment_view, name='order_process_payment'),
    path('success/<str:order_number>/', web_order_success_view, name='order_success'),
]
