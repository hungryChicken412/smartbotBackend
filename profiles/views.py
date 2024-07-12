import json
from operator import indexOf
import re
from urllib import request

from .models import Profile, TestQuestion
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from threading import Thread 
import django_filters.rest_framework
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.csrf import csrf_exempt
from ipware import get_client_ip
from uuid import uuid4





class ProfileMiniViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileMiniSerializer

    def get_queryset(self):
        profile = Profile.objects.all().filter(user=self.request.user)
        print("oln")
        return profile

    permission_classes = [IsAuthenticated]




from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    def get_page_size(self, request):
        return int(request.query_params.get('numberOfQuestions', 3))

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class =  TestQuestionSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {
        'subject': ["in", "exact"],
        'topic': ["in", "exact"],
        'level':["exact"],
        'typeof':["exact"]

    }
    pagination_class = CustomPagination

    def get_queryset(self):
        testID =""
        try:
            testID = self.request.query_params['testID']
            querySet =  Test.objects.get(id=testID).question.all()
            self.request.user.profile.testsAttempted.add(testID)
            self.request.user.profile.save()
            return querySet
        except:
            prevAttempted = self.request.query_params['prevAttempted']
            querySet = TestQuestion.objects.all()
            if (int(prevAttempted) == 0):
                return querySet.exclude(id__in=self.request.user.profile.attempted.all())
            else:
                return querySet
    permission_classes = [IsAuthenticated]


class testSeriesViewSet(viewsets.ModelViewSet):
    serializer_class =  TestSeriesSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = PageNumberPagination
    

    def get_queryset(self):
        testSeries = TestSeries.objects.all()
        return testSeries

        

    permission_classes = [IsAuthenticated]



class practicalViewSet(viewsets.ModelViewSet):
    serializer_class =  practicalSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = PageNumberPagination
    

    def get_queryset(self):
        testSeries =  PracticalSimulation.objects.all()
        return testSeries

        

    #permission_classes = [IsAuthenticated]


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class =  SubjectSerializer
    


    def get_queryset(self):
        questions =  Subject.objects.all()
        return questions

    permission_classes = [IsAuthenticated]




class ProfileEditViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileEditSerializer

    def get_queryset(self):
        profile = Profile.objects.all().filter(user=self.request.user)
        return profile

    permission_classes = [IsAuthenticated]

