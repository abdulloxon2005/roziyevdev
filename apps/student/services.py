from django.db.models import Sum, Count, Q
from django.utils import timezone
from apps.courses.models import Course, Lesson
from apps.learning.models import Enrollment, LessonProgress, Assignment, AssignmentSubmission, SubmissionStatus
from apps.contests.models import Contest, ContestParticipant, ContestStatus
from apps.projects.models import Project, ProjectStatus
from apps.roadmaps.models import RoadmapTrack, RoadmapNode, UserRoadmapProgress


def get_student_overview_stats(user):
    """O'quvchi boshqaruv paneli uchun umumiy statistikalar va tezkor ma'lumotlar."""
    enrollments = Enrollment.objects.filter(user=user).select_related('course', 'course__category', 'last_lesson').order_by('-updated_at')
    enrolled_courses_count = enrollments.count()
    completed_lessons_count = LessonProgress.objects.filter(enrollment__user=user).count()

    submissions = AssignmentSubmission.objects.filter(student=user)
    approved_submissions_count = submissions.filter(status=SubmissionStatus.APPROVED).count()
    pending_submissions_count = submissions.filter(status=SubmissionStatus.PENDING).count()
    rejected_submissions_count = submissions.filter(status=SubmissionStatus.REJECTED).count()

    # Musobaqalar
    now = timezone.now()
    active_contests = Contest.objects.filter(is_published=True, start_time__lte=now, end_time__gte=now).count()
    upcoming_contests = Contest.objects.filter(is_published=True, start_time__gt=now).count()

    # Loyihalar
    my_projects_count = Project.objects.filter(author=user).count()

    return {
        'enrollments': enrollments,
        'enrolled_courses_count': enrolled_courses_count,
        'completed_lessons_count': completed_lessons_count,
        'approved_submissions_count': approved_submissions_count,
        'pending_submissions_count': pending_submissions_count,
        'rejected_submissions_count': rejected_submissions_count,
        'coins': user.coins,
        'active_contests_count': active_contests,
        'upcoming_contests_count': upcoming_contests,
        'my_projects_count': my_projects_count,
    }


def calculate_course_leaderboard(course, current_user=None):
    """
    Muayyan kurs bo'yicha barcha yozilgan talabalar reytingini hisoblaydi:
    XP = (Vazifalar Bali) + (Darslar Progressi % * 5) + (Topshiriqlardan olingan tangalar * 2)
    """
    enrollments = Enrollment.objects.filter(course=course).select_related('user', 'user__profile')
    
    # Ushbu kursdagi barcha qabul qilingan vazifalar
    submissions = AssignmentSubmission.objects.filter(
        assignment__lesson__module__course=course,
        status=SubmissionStatus.APPROVED
    ).values('student_id').annotate(
        total_score=Sum('score'),
        total_coins=Sum('coins_awarded'),
        approved_count=Count('id')
    )
    
    sub_map = {
        s['student_id']: {
            'score': s['total_score'] or 0,
            'coins': s['total_coins'] or 0,
            'count': s['approved_count'] or 0,
        }
        for s in submissions
    }

    leaderboard = []
    for enr in enrollments:
        student = enr.user
        sub_data = sub_map.get(student.id, {'score': 0, 'coins': 0, 'count': 0})
        
        progress_points = int(enr.progress_percent * 5)
        assignment_points = sub_data['score']
        coin_points = sub_data['coins'] * 2
        total_xp = assignment_points + progress_points + coin_points

        leaderboard.append({
            'user': student,
            'progress_percent': enr.progress_percent,
            'is_completed': enr.is_completed,
            'assignment_score': assignment_points,
            'assignments_count': sub_data['count'],
            'coins_earned': sub_data['coins'],
            'total_xp': total_xp,
        })

    # Saralash: XP kamayish tartibida, keyin progress, keyin topshirilgan vazifalar
    leaderboard.sort(key=lambda x: (x['total_xp'], x['progress_percent'], x['assignments_count']), reverse=True)

    # O'rinlarni belgilash va ligalarga ajratish
    total_participants = len(leaderboard)
    current_user_rank_data = None

    for idx, item in enumerate(leaderboard, start=1):
        item['rank'] = idx
        
        # Liga belgilash (Diamond, Gold, Silver, Bronze)
        if idx <= max(1, int(total_participants * 0.05)):
            item['tier'] = 'Diamond'
            item['tier_badge'] = 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30'
        elif idx <= max(2, int(total_participants * 0.20)):
            item['tier'] = 'Gold'
            item['tier_badge'] = 'text-amber-400 bg-amber-500/10 border-amber-500/30'
        elif idx <= max(3, int(total_participants * 0.50)):
            item['tier'] = 'Silver'
            item['tier_badge'] = 'text-slate-300 bg-slate-500/10 border-slate-500/30'
        else:
            item['tier'] = 'Bronze'
            item['tier_badge'] = 'text-orange-400 bg-orange-500/10 border-orange-500/30'

        if current_user and item['user'].id == current_user.id:
            current_user_rank_data = item
            # Keyingi o'rindagi talaba bilan farq
            if idx > 1:
                item['points_to_next'] = leaderboard[idx - 2]['total_xp'] - item['total_xp'] + 5
            else:
                item['points_to_next'] = 0

    return {
        'leaderboard': leaderboard,
        'top_three': leaderboard[:3],
        'total_participants': total_participants,
        'current_user_rank_data': current_user_rank_data,
    }


def sync_roadmap_with_user_progress(user, track):
    """
    O'quvchi tomonidan platformada darslar o'zlashtirilganda yoki vazifalar topshirilganda,
    Roadmap bekatlarini avtomatik sinxronlab 'completed' yoki 'in_progress' holatga o'tkazadi.
    """
    nodes = RoadmapNode.objects.filter(stage__track=track).select_related('linked_lesson', 'linked_course', 'stage')
    completed_lesson_ids = set(
        LessonProgress.objects.filter(enrollment__user=user).values_list('lesson_id', flat=True)
    )

    user_progress_map = {
        up.node_id: up
        for up in UserRoadmapProgress.objects.filter(user=user, node__stage__track=track)
    }

    first_uncompleted_found = False

    for node in nodes:
        is_completed = False
        if node.linked_lesson_id and node.linked_lesson_id in completed_lesson_ids:
            is_completed = True

        progress_obj = user_progress_map.get(node.id)
        if not progress_obj:
            new_status = 'completed' if is_completed else ('in_progress' if not first_uncompleted_found else 'locked')
            progress_obj = UserRoadmapProgress.objects.create(
                user=user,
                node=node,
                status=new_status,
                completed_at=timezone.now() if is_completed else None
            )
            user_progress_map[node.id] = progress_obj
        else:
            if is_completed and progress_obj.status != 'completed':
                progress_obj.status = 'completed'
                progress_obj.completed_at = timezone.now()
                progress_obj.save(update_fields=['status', 'completed_at'])

        if progress_obj.status != 'completed' and not first_uncompleted_found:
            first_uncompleted_found = True
            if progress_obj.status == 'locked':
                progress_obj.status = 'in_progress'
                progress_obj.save(update_fields=['status'])

    # Umumiy foizni hisoblash
    total_nodes = len(nodes)
    completed_nodes = sum(1 for p in user_progress_map.values() if p.status == 'completed')
    percent = int((completed_nodes / total_nodes) * 100) if total_nodes > 0 else 0

    return {
        'nodes_progress_map': user_progress_map,
        'total_nodes': total_nodes,
        'completed_nodes': completed_nodes,
        'percent': percent,
    }
