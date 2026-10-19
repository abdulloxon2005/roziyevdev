from django.urls import path
from .views import (
    OrderListCreateAPIView,
    OrderDetailAPIView,
    SimulatePaymentAPIView,
)

urlpatterns = [
    # REST API endpoints
    path('', OrderListCreateAPIView.as_view(), name='api_order_list_create'),
    path('<str:order_number>/', OrderDetailAPIView.as_view(), name='api_order_detail'),
    path('<str:order_number>/simulate-pay/', SimulatePaymentAPIView.as_view(), name='api_order_simulate_pay'),

    # Eski /api/ prefiksi bilan moslik (Backwards compatibility)
    path('api/orders/', OrderListCreateAPIView.as_view()),
    path('api/orders/<str:order_number>/', OrderDetailAPIView.as_view()),
    path('api/orders/<str:order_number>/simulate-pay/', SimulatePaymentAPIView.as_view()),
]
