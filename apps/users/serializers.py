from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema_field
from .models import CustomUser, Profile, UserRole


class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.CharField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'avatar',
            'avatar_url',
            'headline',
            'bio',
            'github',
            'linkedin',
            'telegram',
            'website',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'display_name',
            'phone',
            'role',
            'date_joined',
            'profile',
        ]
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'phone', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Kiritilgan parollar bir-biriga mos kelmadi."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            role=UserRole.STUDENT,
        )
        return user


class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    headline = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    github = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    linkedin = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    telegram = serializers.CharField(required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    avatar = serializers.ImageField(required=False, allow_null=True)

    def update(self, user, validated_data):
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.phone = validated_data.get('phone', user.phone)
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.headline = validated_data.get('headline', profile.headline)
        profile.bio = validated_data.get('bio', profile.bio)
        profile.github = validated_data.get('github', profile.github)
        profile.linkedin = validated_data.get('linkedin', profile.linkedin)
        profile.telegram = validated_data.get('telegram', profile.telegram)
        profile.website = validated_data.get('website', profile.website)
        if 'avatar' in validated_data and validated_data['avatar'] is not None:
            profile.avatar = validated_data['avatar']
        profile.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Yangi parollar mos kelmadi."})
        return attrs
