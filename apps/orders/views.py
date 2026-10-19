from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.courses.models import Course
from apps.learning.models import Enrollment
from apps.learning.services import enroll_user, get_enrollment
from .models import Order, OrderStatus, PaymentMethod
from .serializers import OrderSerializer, CreateOrderSerializer


# ==============================================================================
# WEB VIEWS
# ==============================================================================

@login_required
def web_checkout_view(request, slug):
    """Kursni sotib olish sahifasi (Checkout)."""
    course = get_object_or_404(Course, slug=slug, is_published=True)

    # Agar foydalanuvchi allaqachon a'zo bo'lsa
    existing_enrollment = get_enrollment(request.user, course)
    if existing_enrollment:
        messages.info(request, "Siz ushbu kursga allaqachon yozilgansiz.")
        return redirect('course_learn', slug=course.slug)

    # Agar kurs bepul bo'lsa, to'g'ridan-to'g'ri a'zo qilish
    if course.is_free or course.price <= 0:
        enroll_user(request.user, course)
        messages.success(request, f"Tabriklaymiz! Siz '{course.title}' bepul kursiga a'zo bo'ldingiz.")
        return redirect('course_learn', slug=course.slug)

    # Kutilayotgan buyurtmani topish yoki yangisini yaratish
    order = Order.objects.filter(
        user=request.user,
        course=course,
        status=OrderStatus.PENDING
    ).first()

    if not order:
        order = Order.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method=PaymentMethod.TEST_DEMO,
        )

    context = {
        'course': course,
        'order': order,
        'payment_methods': PaymentMethod.choices,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
@require_POST
def web_process_payment_view(request, order_number):
    """To'lovni qayta ishlash / tasdiqlash harakati."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if order.status == OrderStatus.PAID:
        return redirect('order_success', order_number=order.order_number)

    payment_method = request.POST.get('payment_method', PaymentMethod.TEST_DEMO)
    order.payment_method = payment_method

    # Sinov to'lovi yoki to'lov simulyatsiyasi
    order.mark_as_paid()
    messages.success(request, "To'lov muvaffaqiyatli qabul qilindi! Kurs darslariga xush kelibsiz.")
    return redirect('order_success', order_number=order.order_number)


@login_required
def web_order_success_view(request, order_number):
    """Muvaffaqiyatli xarid sahifasi."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
        'course': order.course,
    }
    return render(request, 'orders/success.html', context)


# ==============================================================================
# REST API VIEWS
# ==============================================================================

class OrderListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request):
        orders = Order.objects.filter(user=request.user).select_related('course')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @extend_schema(request=CreateOrderSerializer, responses={201: OrderSerializer})
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = get_object_or_404(Course, id=serializer.validated_data['course_id'], is_published=True)

        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response(
                {"detail": "Siz allaqachon ushbu kursga yozilgansiz."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method=serializer.validated_data.get('payment_method', PaymentMethod.TEST_DEMO)
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: OrderSerializer})
    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        return Response(OrderSerializer(order).data)


class SimulatePaymentAPIView(APIView):
    """Test rejimida buyurtmani to'langan deb tasdiqlash API'si."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    @extend_schema(request=None, responses={200: OrderSerializer})
    def post(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        order.mark_as_paid()
        return Response({
            "message": "To'lov muvaffaqiyatli amalga oshirildi.",
            "order": OrderSerializer(order).data
        })

