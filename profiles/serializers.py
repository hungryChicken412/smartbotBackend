from dataclasses import field
from rest_framework import serializers
from .models import *
from datetime import datetime, timedelta


# Serializers define the API representation.
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'username',
            'avatar',
            'first_name',
            'last_name',
            'email',
            'companyUrl',
            'credits',
            'subscriptionPlan',
            'build', 'ready', 'failed', 'pending',

        ]


class ProfileMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'username',
            'avatar',
            'email',

        ]


class ProfileEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'companyUrl', 'created', 'email_confirmed'

        ]


class ChatbotMiniSerializer(serializers.ModelSerializer):
    interactions = serializers.SerializerMethodField()

    def get_interactions(self, obj):
        print(obj.logs)
        return obj.logs.count()

    class Meta:
        model = Chatbot
        fields = [
            'name',
            'created',
            'status',
            'website',
            'id',
            'interactions'

        ]


class ChatbotAnalyticalSerializer(serializers.ModelSerializer):
    interactions = serializers.SerializerMethodField()

    def get_interactions(self, obj):
        intr = {
            'total': obj.logs.count(),
            'last_week': {},
            'last_week_total': 0,
            'week_before_last': 0,

            'growth': 0

        }

        last7Days = datetime.now().date() - timedelta(days=7)
        last14Days = datetime.now().date() - timedelta(days=14)
        for i in obj.logs.all():

            if i.time.date() > last7Days:

                intr['last_week_total'] += 1
                try:
                    intr['last_week'][str(i.time.date())] += 1
                except:
                    intr['last_week'][str(i.time.date())] = 1
            if last14Days < i.time.date() and i.time.date() < last7Days:
                intr['week_before_last'] += 1

        if intr['week_before_last'] > 0:
            intr['growth'] = (len(intr['last_week']) / intr['week_before_last']
                              ) * 100
        else:
            intr['growth'] = 100

        return intr

    class Meta:
        model = Chatbot
        fields = [
            'name',
            'created',
            'status',
            'website',
            'id',
            'interactions'

        ]


class ChatbotEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chatbot
        fields = [
            'name',
            'created',
            'status',
            'website',
            'avatar',
            'caching', 'chatbotData', 'tokenID', 'article'


        ]


class ChatbotHostSerializer(serializers.ModelSerializer):
    sessionID = serializers.SerializerMethodField()

    def get_sessionID(self, obj):
        return ''

    class Meta:
        model = Chatbot
        fields = [
            'name',
            'website',
            'avatar', 'caching', 'chatbotHostData', 'sessionID'

        ]


class HelpdeskTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = IssueTicket
        fields = [
            'logs', 'time',
            'user', 'bot',
            'state',

        ]
