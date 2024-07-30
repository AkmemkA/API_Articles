from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Article

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def validate_password(self, value):
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one number.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one letter.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'is_private', 'author']
