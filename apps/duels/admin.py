from django.contrib import admin
from .models import Duel, DuelChallenge, DuelStats

admin.site.register(DuelChallenge)
admin.site.register(DuelStats)
admin.site.register(Duel)
