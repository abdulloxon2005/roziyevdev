import uuid
from django.db import models, transaction
from django.utils import timezone
from apps.core.models import TimeStampedModel
from apps.users.models import CustomUser
from apps.courses.models import Course
from apps.learning.services import enroll_user


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Kutilmoqda'
    PAID = 'paid', 'To\'langan'
    FAILED = 'failed', 'Xatolik'
    CANCELLED = 'cancelled', 'Bekor qilingan'


class PaymentMethod(models.TextChoices):
    TEST_DEMO = 'test_demo', 'Sinov to\'lovi (Demo)'
    CLICK = 'click', 'Click'
    PAYME = 'payme', 'Payme'
    UZUM = 'uzum', 'Uzum Bank'


def generate_order_number():
    code = uuid.uuid4().hex[:8].upper()
    date_str = timezone.now().strftime('%Y%m%d')
    return f"ORD-{date_str}-{code}"


class Order(TimeStampedModel):
    order_number = models.CharField(
        max_length=40,
        unique=True,
        default=generate_order_number,
        verbose_name="Buyurtma raqami"
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Foydalanuvchi"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Kurs"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="Summa (so'm)"
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Holati"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.TEST_DEMO,
        verbose_name="To'lov tizimi"
    )
    transaction_id = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Tranzaksiya ID"
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="To'langan vaqt"
    )

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} - {self.user.email} - {self.course.title} ({self.get_status_display()})"

    @transaction.atomic
    def mark_as_paid(self, transaction_id=None):
        """Buyurtmani to'langan deb belgilash va talabani kursga yozish."""
        if self.status == OrderStatus.PAID:
            return False
        self.status = OrderStatus.PAID
        self.paid_at = timezone.now()
        if transaction_id:
            self.transaction_id = transaction_id
        elif not self.transaction_id:
            self.transaction_id = f"TRX-{uuid.uuid4().hex[:12].upper()}"
        self.save(update_fields=['status', 'paid_at', 'transaction_id', 'updated_at'])

        # Talabani kursga yozish
        enroll_user(self.user, self.course)
        return True
