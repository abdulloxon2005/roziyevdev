from rest_framework import serializers
from .models import Order
from apps.courses.serializers import CourseListSerializer


class OrderSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'course',
            'course_title',
            'amount',
            'status',
            'status_display',
            'payment_method',
            'payment_method_display',
            'transaction_id',
            'paid_at',
            'created_at',
        ]
        read_only_fields = ['id', 'order_number', 'status', 'transaction_id', 'paid_at', 'created_at']


class CreateOrderSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=['test_demo', 'click', 'payme', 'uzum'], default='test_demo')
