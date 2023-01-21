
from dataclasses import field
from rest_framework import serializers
from .models import BlogPost


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = [
            'title',
            'published',
            'brief',
            'background',
            'id'
        ]


class BlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = [
            'title',
            'published',
            'background',
            'brief',
            'content',
        ]
