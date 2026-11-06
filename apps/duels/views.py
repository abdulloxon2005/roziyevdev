import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.learning.models import Enrollment
from apps.users.models import CustomUser
from .challenges import ensure_challenges
from .models import DIFFICULTY_POINTS, Difficulty, Duel, DuelChallenge, DuelStats, DuelStatus


def _touch(user):
    stats, _ = DuelStats.objects.get_or_create(user=user)
    stats.last_seen = timezone.now()
    stats.save(update_fields=['last_seen'])
    return stats


def _run_tests(code, challenge):
    """Talaba kodini topshiriq testlari bilan mavjud sandbox ichida tekshiradi."""
    from apps.student.views import _execute_code_safely
    harness = (
        "\n\nTESTS = " + repr([(list(a), e) for a, e in challenge.tests]) + "\n"
        "PASSED = 0\n"
        "for ARGS, EXPECTED in TESTS:\n"
        "    try:\n"
        "        if solve(*ARGS) == EXPECTED:\n"
        "            PASSED += 1\n"
        "    except Exception:\n"
        "        pass\n"
        "print('RESULT', PASSED, len(TESTS))\n"
    )
    output, ok, _ = _execute_code_safely('python', code + harness)
    for line in output.splitlines():
        if line.startswith('RESULT '):
            _, passed, total = line.split()
            return int(passed), int(total), ''
    return 0, len(challenge.tests), output.strip()[-400:]


@login_required
def duel_home_view(request):
    ensure_challenges()
    me = request.user
    _touch(me)

    my_course_ids = list(Enrollment.objects.filter(user=me).values_list('course_id', flat=True))
    rivals_qs = (
        CustomUser.objects.filter(enrollments__course_id__in=my_course_ids)
        .exclude(id=me.id).distinct().select_related('duel_stats', 'profile')
    )
    rivals = []
    for u in rivals_qs:
        stats = getattr(u, 'duel_stats', None)
        shared = Enrollment.objects.filter(user=u, course_id__in=my_course_ids).select_related('course')
        rivals.append({
            'user': u,
            'points': stats.points if stats else 0,
            'wins': stats.wins if stats else 0,
            'losses': stats.losses if stats else 0,
            'online': stats.is_online if stats else False,
            'courses': [e.course.title for e in shared],
            'progress': max((e.progress_percent for e in shared), default=0),
        })
    rivals.sort(key=lambda r: (not r['online'], -r['points']))

    active = Duel.objects.filter(
        Q(challenger=me) | Q(opponent=me), status=DuelStatus.ACTIVE
    ).select_related('challenger', 'opponent').first()
    incoming = Duel.objects.filter(opponent=me, status=DuelStatus.PENDING).select_related('challenger', 'challenge')
    outgoing = Duel.objects.filter(challenger=me, status=DuelStatus.PENDING).select_related('opponent')
    history = Duel.objects.filter(
        Q(challenger=me) | Q(opponent=me), status=DuelStatus.FINISHED
    ).select_related('challenger', 'opponent', 'winner', 'challenge')[:10]
    my_stats = DuelStats.objects.get(user=me)
    top = DuelStats.objects.select_related('user').order_by('-points')[:5]

    return render(request, 'duels/home.html', {
        'rivals': rivals, 'active': active, 'incoming': incoming, 'outgoing': outgoing,
        'history': history, 'my_stats': my_stats, 'top': top,
        'has_courses': bool(my_course_ids), 'difficulties': Difficulty.choices,
        'active_menu': 'duel',
    })


@login_required
@require_POST
def duel_send_view(request):
    ensure_challenges()
    opponent = get_object_or_404(CustomUser, id=request.POST.get('opponent_id') or 0)
    difficulty = request.POST.get('difficulty')
    me = request.user
    if opponent.id == me.id or difficulty not in dict(Difficulty.choices):
        messages.error(request, "Noto'g'ri so'rov.")
        return redirect('duel_home')
    my_courses = Enrollment.objects.filter(user=me).values('course_id')
    if not Enrollment.objects.filter(user=opponent, course_id__in=my_courses).exists():
        messages.error(request, "Faqat o'z yo'nalishingizdagi talabalarga so'rov yuborishingiz mumkin.")
        return redirect('duel_home')
    if Duel.objects.filter(challenger=me, opponent=opponent, status=DuelStatus.PENDING).exists():
        messages.info(request, "Bu talabaga so'rov allaqachon yuborilgan.")
        return redirect('duel_home')
    challenge = random.choice(list(DuelChallenge.objects.filter(difficulty=difficulty)))
    Duel.objects.create(challenger=me, opponent=opponent, challenge=challenge, difficulty=difficulty)
    messages.success(request, f"{opponent.display_name}ga duel so'rovi yuborildi. Tasdiqlashini kuting.")
    return redirect('duel_home')


@login_required
@require_POST
def duel_respond_view(request, duel_id):
    action = request.POST.get('action')
    with transaction.atomic():
        duel = get_object_or_404(Duel.objects.select_for_update(), id=duel_id)
        me = request.user
        if duel.status != DuelStatus.PENDING:
            return redirect('duel_home')
        if action == 'cancel' and duel.challenger_id == me.id:
            duel.status = DuelStatus.CANCELLED
        elif duel.opponent_id == me.id and action == 'decline':
            duel.status = DuelStatus.DECLINED
        elif duel.opponent_id == me.id and action == 'accept':
            duel.status = DuelStatus.ACTIVE
            duel.started_at = timezone.now()
        else:
            return redirect('duel_home')
        duel.save()
    if duel.status == DuelStatus.ACTIVE:
        return redirect('duel_room', duel_id=duel.id)
    return redirect('duel_home')


@login_required
def duel_room_view(request, duel_id):
    duel = get_object_or_404(Duel.objects.select_related('challenger', 'opponent', 'challenge'), id=duel_id)
    if not duel.involves(request.user):
        return redirect('duel_home')
    _touch(request.user)
    return render(request, 'duels/room.html', {
        'duel': duel, 'rival': duel.other(request.user), 'challenge': duel.challenge,
        'points': DIFFICULTY_POINTS[duel.difficulty], 'active_menu': 'duel',
    })


@login_required
def duel_state_view(request, duel_id):
    duel = get_object_or_404(Duel, id=duel_id)
    if not duel.involves(request.user):
        return JsonResponse({'error': 'forbidden'}, status=403)
    _touch(request.user)
    return JsonResponse({
        'status': duel.status,
        'winner_id': duel.winner_id,
        'me_id': request.user.id,
    })


@login_required
@require_POST
def duel_submit_view(request, duel_id):
    duel = get_object_or_404(Duel.objects.select_related('challenge'), id=duel_id)
    me = request.user
    if not duel.involves(me):
        return JsonResponse({'error': 'forbidden'}, status=403)
    if duel.status != DuelStatus.ACTIVE:
        return JsonResponse({'status': duel.status, 'winner_id': duel.winner_id, 'me_id': me.id})
    code = (request.POST.get('code') or '')[:20000]
    passed, total, error = _run_tests(code, duel.challenge)
    won = False
    if passed == total:
        with transaction.atomic():
            locked = Duel.objects.select_for_update().get(id=duel.id)
            if locked.status == DuelStatus.ACTIVE:
                locked.status = DuelStatus.FINISHED
                locked.winner = me
                locked.finished_at = timezone.now()
                locked.save()
                won = True
                loser = locked.other(me)
                w, _ = DuelStats.objects.get_or_create(user=me)
                l, _ = DuelStats.objects.get_or_create(user=loser)
                w.points += DIFFICULTY_POINTS[locked.difficulty]
                w.wins += 1
                w.save()
                l.losses += 1
                l.save()
    return JsonResponse({
        'passed': passed, 'total': total, 'error': error, 'won': won,
        'status': Duel.objects.get(id=duel.id).status,
    })


@login_required
def duel_ping_view(request):
    _touch(request.user)
    return JsonResponse({'ok': True})
