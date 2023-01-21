import json
from operator import indexOf
import re
from urllib import request

from .models import Profile
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from threading import Thread
from django.views.decorators.csrf import csrf_exempt
from ipware import get_client_ip
from uuid import uuid4


class ProfileMiniViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileMiniSerializer

    def get_queryset(self):
        profile = Profile.objects.all().filter(user=self.request.user)
        return profile

    permission_classes = [IsAuthenticated]


class ProfileEditViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileEditSerializer

    def get_queryset(self):
        profile = Profile.objects.all().filter(user=self.request.user)
        return profile

    permission_classes = [IsAuthenticated]


class ChatbotMiniViewset(viewsets.ModelViewSet):
    serializer_class = ChatbotMiniSerializer

    def get_queryset(self):
        bots = Chatbot.objects.all().filter(parent=self.request.user)
        return bots

    permission_classes = [IsAuthenticated]


class ChatbotAnalyticalViewset(viewsets.ModelViewSet):
    serializer_class = ChatbotAnalyticalSerializer

    def get_queryset(self):
        bots = Chatbot.objects.all().filter(parent=self.request.user)
        return bots

    permission_classes = [IsAuthenticated]


class ChatbotEditViewset(viewsets.ModelViewSet):
    serializer_class = ChatbotEditSerializer

    def get_queryset(self):

        bots = Chatbot.objects.all().filter(
            parent=self.request.user, id=self.kwargs['id'])
        return bots

    permission_classes = [IsAuthenticated]


class chatbotDeleteViewset(viewsets.ModelViewSet):
    serializer_class = ChatbotEditSerializer

    def get_queryset(self):

        id = self.kwargs['id']

        bots = Chatbot.objects.get(id=id)
        for i in bots.logs.all():
            i.delete()

        bots.delete()
        return []

    permission_classes = [IsAuthenticated]


class chatbotHostViewset(viewsets.ModelViewSet):
    serializer_class = ChatbotHostSerializer

    def get_queryset(self):

        bots = Chatbot.objects.all().filter(tokenID=self.kwargs['id'])
        print(bots[0].status)

        if self.request.headers['Origin'] != bots[0].website or bots[0].status != "Online":
            pass
            # return []

        ip, _is_routable = get_client_ip(self.request)
        if ip is not None:
            log = AnalyticsLog.objects.create(
                user_ip=ip)
            bots[0].logs.add(log)
            bots[0].save()
            log.save()

        return bots

    permission_classes = [permissions.AllowAny]


class HelpdeskTicketViewset(viewsets.ModelViewSet):
    serializer_class = HelpdeskTicketSerializer

    def get_queryset(self):
        tickets = IssueTicket.objects.all().filter(
            user=self.request.user)
        return tickets

    permission_classes = [IsAuthenticated]
