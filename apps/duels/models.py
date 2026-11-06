from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel
from apps.users.models import CustomUser


class Difficulty(models.TextChoices):
    EASY = 'easy', 'Oson'
    MEDIUM = 'medium', "O'rta"
    HARD = 'hard', 'Qiyin'


DIFFICULTY_POINTS = {'easy': 10, 'medium': 20, 'hard': 30}
ONLINE_WINDOW_SECONDS = 60


class DuelChallenge(TimeStampedModel):
    """Duelda ikkala talabaga beriladigan bir xil topshiriq (Python funksiyasi)."""
    title = models.CharField(max_length=150)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    starter_code = models.TextField(default="def solve(x):\n    # Kodingizni shu yerga yozing\n    pass\n")
    tests = models.JSONField(default=list, help_text="[[argumentlar ro'yxati, kutilgan natija], ...]")

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"


class DuelStats(TimeStampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='duel_stats')
    points = models.IntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    last_seen = models.DateTimeField(null=True, blank=True)

    @property
    def is_online(self):
        return bool(self.last_seen) and (timezone.now() - self.last_seen).total_seconds() < ONLINE_WINDOW_SECONDS

    def __str__(self):
        return f"{self.user.email}: {self.points}"


class DuelStatus(models.TextChoices):
    PENDING = 'pending', 'Javob kutilmoqda'
    ACTIVE = 'active', 'Davom etmoqda'
    FINISHED = 'finished', 'Tugagan'
    DECLINED = 'declined', 'Rad etilgan'
    CANCELLED = 'cancelled', 'Bekor qilingan'


class Duel(TimeStampedModel):
    challenger = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='duels_sent')
    opponent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='duels_received')
    challenge = models.ForeignKey(DuelChallenge, on_delete=models.PROTECT, related_name='duels')
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    status = models.CharField(max_length=10, choices=DuelStatus.choices, default=DuelStatus.PENDING)
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='duels_won')
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def involves(self, user):
        return user.id in (self.challenger_id, self.opponent_id)

    def other(self, user):
        return self.opponent if user.id == self.challenger_id else self.challenger

    def __str__(self):
        return f"{self.challenger.email} vs {self.opponent.email} [{self.status}]"
