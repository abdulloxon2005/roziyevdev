from rest_framework import serializers
from .models import Category, Course, CourseModule, Lesson
from apps.users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    courses_count = serializers.IntegerField(source='courses.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'order', 'courses_count']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'duration_minutes', 'is_preview', 'order']


class CourseModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = CourseModule
        fields = ['id', 'title', 'order', 'lessons']


class CourseListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    formatted_price = serializers.CharField(read_only=True)
    thumbnail_url = serializers.CharField(read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'slug',
            'category_name',
            'category_slug',
            'short_description',
            'thumbnail_url',
            'level',
            'level_display',
            'price',
            'formatted_price',
            'is_free',
            'duration_hours',
            'is_featured',
            'rating',
            'students_count',
            'created_at',
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructor = UserSerializer(read_only=True)
    modules = CourseModuleSerializer(many=True, read_only=True)
    formatted_price = serializers.CharField(read_only=True)
    thumbnail_url = serializers.CharField(read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    learn_points = serializers.ListField(child=serializers.CharField(), read_only=True)
    requirement_points = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'instructor',
            'short_description',
            'description',
            'thumbnail_url',
            'level',
            'level_display',
            'price',
            'formatted_price',
            'is_free',
            'duration_hours',
            'learn_points',
            'requirement_points',
            'is_featured',
            'rating',
            'students_count',
            'modules',
            'created_at',
            'updated_at',
        ]
