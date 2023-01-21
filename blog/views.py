

from .models import BlogPost
from .serializers import *
from rest_framework.authentication import TokenAuthentication

from rest_framework import routers, serializers, viewsets, generics
from threading import Thread
from django.views.decorators.csrf import csrf_exempt


class BlogViewset(viewsets.ModelViewSet):
    serializer_class = BlogSerializer

    def get_queryset(self):
        profile = BlogPost.objects.all()
        return profile


class BlogPostViewset(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        profile = BlogPost.objects.all()
        return profile


# Create your views here.
