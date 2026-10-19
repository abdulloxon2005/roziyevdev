from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser
from apps.courses.models import Course, Category
from apps.orders.models import Order, OrderStatus, PaymentMethod
from apps.learning.models import Enrollment


class OrdersTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="buyer_test",
            email="buyer@example.com",
            password="password123"
        )
        self.category = Category.objects.create(name="Mobile", slug="mobile")
        self.course = Course.objects.create(
            title="Paid Flutter Course",
            slug="paid-flutter",
            category=self.category,
            price=250000,
            is_free=False
        )

    def test_checkout_page(self):
        self.client.login(email="buyer@example.com", password="password123")
        response = self.client.get(reverse('order_checkout', args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Paid Flutter Course")
        self.assertTrue(Order.objects.filter(user=self.user, course=self.course).exists())

    def test_order_payment_and_auto_enrollment(self):
        order = Order.objects.create(
            user=self.user,
            course=self.course,
            amount=self.course.price,
            payment_method=PaymentMethod.TEST_DEMO
        )
        self.assertFalse(Enrollment.objects.filter(user=self.user, course=self.course).exists())

        order.mark_as_paid()
        self.assertEqual(order.status, OrderStatus.PAID)
        self.assertTrue(order.paid_at is not None)
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.course).exists())
