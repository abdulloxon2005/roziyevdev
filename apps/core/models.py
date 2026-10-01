from django.db import models


class TimeStampedModel(models.Model):
    """
    Barcha modellar uchun umumiy yaratilgan va yangilangan vaqtlarni saqlovchi mavhum model.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    class Meta:
        abstract = True
