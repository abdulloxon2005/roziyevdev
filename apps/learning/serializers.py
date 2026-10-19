from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Enrollment, LessonProgress
from apps.courses.models import Lesson, CourseModule, Course


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source='lesson.id', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson_id', 'lesson_title', 'created_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)
    thumbnail_url = serializers.CharField(source='course.thumbnail_url', read_only=True)
    is_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'course',
            'course_title',
            'course_slug',
            'thumbnail_url',
            'progress_percent',
            'completed_at',
            'is_completed',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['progress_percent', 'completed_at', 'is_completed']


class LessonLearningSerializer(serializers.ModelSerializer):
    embed_url = serializers.CharField(read_only=True)
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'lesson_type',
            'duration_minutes',
            'video_url',
            'embed_url',
            'content',
            'attachment',
            'source_code_url',
            'is_preview',
            'order',
            'is_completed',
        ]

    @extend_schema_field(serializers.BooleanField())
    def get_is_completed(self, obj):
        enrollment = self.context.get('enrollment')
        if not enrollment:
            return False
        completed_ids = self.context.get('completed_lesson_ids', set())
        return obj.id in completed_ids

