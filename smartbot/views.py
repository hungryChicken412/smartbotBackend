
from .tokens import account_activation_token
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth.models import User
from profiles.models import *
from profiles.serializers import ProfileSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage
from .settings import EMAIL_HOST_USER
from django.shortcuts import render
from django.core.mail import send_mail
import uuid
from .utils import *
import requests
import numpy as np
# Register user rest api view


website = "https://orangewaves.tech"


class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data
            # first_name = data['firstName'] if data['firstName'] != None else ''
            # last_name = data['lastName'] if data['lastName'] != None else ''
            first_name = ''
            last_name = ''
            email = data['email']
            password = data['password']
            password2 = data['password2']
            username = data['username']

            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            if password != password2:
                return Response({'error': 'Please provide both username and password'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                if len(password) >= 8:
                    if not User.objects.filter(username=username, email=email).exists():
                        user = User.objects.create_user(
                            username=username,
                            password=password,
                            email=email,
                            first_name=first_name,
                            last_name=last_name)

                        user.save()
                        subject = 'Account Activation'
                        activate_url = "https://api.orangewaves.tech/"+'activate/' + \
                            str(user.pk) + '/' + \
                            account_activation_token.make_token(user)+'/'
                        message = f"""
                       Hey there{username},
                       Thank you for signing up for OrangeWavesAI,
                          Please click on the link below to activate your account
                            {activate_url}

                        Regards,
                        Team OrangeWavesAI


                        """
                        user.email_user(subject, message)

                        if Profile.objects.filter(user=user).exists():
                            profile = Profile.objects.get(user=user)
                            # print(data['companyUrl'])
                            # profile.companyUrl = data['companyUrl'] if data['companyUrl'] != None else ''
                            profile.save()

                        if User.objects.filter(username=username).exists():
                            return Response({'success': 'User created successfully'},
                                            status=status.HTTP_201_CREATED)
                    else:
                        return Response({'error': 'User already exists'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Password must be at least 8 characters'},
                                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileUpdateUserVew(APIView):
    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            data = request.data
            user = profile.user

            if data['first_name'] != '':
                user.first_name = str(data['first_name'])
                profile.first_name = data['first_name']
            if data['last_name'] != '':
                user.last_name = data['last_name']
                profile.last_name = data['last_name']
            if data['username'] != '':
                user.username = data['username']
                profile.username = data['username']

            user.save()

            if data['companyUrl'] != '':
                profile.companyUrl = data['companyUrl']
            if data['planType'] != 'Select A Plan':
                # profile.subscriptionPlan = SubscriptionPlan.objects.get(id=data['planType'])
                pass

            profile.save()

            return Response({'success': 'User updated successfully'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidateToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        data = request.data

        token = data

        if Token.objects.filter(key=token).exists():
            return Response({
                'status': 'success',
                'msg': 'Token is valid',
            },
                status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'failed',
                'msg': 'Token is invalid',
            },
                status=status.HTTP_400_BAD_REQUEST)


class ChatbotUpdate(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):

        data = request.data
        data = json.loads(request.data['body'])

        details = data['details']

        try:
            chatbot = Chatbot.objects.get(id=data['id'], parent=request.user)

            chatbot.chatbotData = request.data['body']
            chatbot.status = details['status']

            chatbot.save()
        except Exception as e:
            print(e)
            chatbot = Chatbot.objects.create(
                chatbotData=request.data['body'], parent=request.user, tokenID=str(uuid.uuid4()))

        chatbot.chatbotHostData = processChatbotData(data)

        if (details['article']):
            chatbot.article = details['article']
        if (details['name']):
            chatbot.name = details['name']
        if (details['caching']):
            chatbot.caching = details['caching']
        if (details['website']):
            chatbot.website = details['website']
        try:
            if (request.FILES):
                chatbot.avatar = request.FILES['avatar']
        except:
            pass

        chatbot.save()
        return Response({'id': chatbot.id}, status=status.HTTP_200_OK)


class logSession(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        data = request.data

        try:
            chatbot = Chatbot.objects.get(token=data['id'])
            chatbot.logs.get(sessionID=data['sessionID'])
        except Exception as e:
            chatbot = Chatbot.objects.create(
                chatbotData=request.data['body'], parent=request.user, tokenID=str(uuid.uuid4()))

        return Response({'id': chatbot.id}, status=status.HTTP_200_OK)


class OpenHelpdeskTicket(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        data = request.data
        try:
            chatbot = Chatbot.objects.get(tokenID=data['id'])
            ticket = IssueTicket.objects.create(
                user=chatbot.parent,
                logs=data['logs'],
                bot=chatbot,
                state='Pending',
                ticketID=str(uuid.uuid4().hex[:10].upper())
            )
            ticket.save()

            return Response({'success': 'Ticket created successfully', 'issueID':   ticket.ticketID}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class sendEmail(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        data = request.data
        to = data['to']
        subject = data['subject']
        message = data['message']

        try:
            send_mail(subject, message, 'Notifications ',
                      [to], fail_silently=False)
            return Response({'success': 'Email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SentimentAnalysis(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        data = request.data
        text = data['text']

        complaint_sentences = [
            'I want to file a complaint',
            'I want to log a ticket',
            'I want to report a bug',
            'I want to report a problem',
            'I want to log a problem',
            'I want to issue a ticket',
            'I want to issue a complaint',

        ]
        appointment_sentences = [
            'I want to book an appointment',
            'I want to schedule an appointment',
            'I want to make an appointment',
            'I want to book a meeting',
            'I want to talk to support',
            'I want to talk to a support agent',
            'I want to talk to a support representative',
            'I want to talk to a support executive',
            'I want to talk to a customer service',
        ]

        try:

            API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
            headers = {
                "Authorization": "Bearer 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"}

            def query(payload):
                response = requests.post(
                    API_URL, headers=headers, json=payload)
                return response.json()

            complaint_score = query({
                "inputs": {
                    "source_sentence": text,
                    "sentences": complaint_sentences
                },
            })

            appointment_score = query({
                "inputs": {
                    "source_sentence": text,
                    "sentences": appointment_sentences
                },
            })

            threshold = 0.6

            # maximum of each list
            complaint_max = max(complaint_score)
            appointment_max = max(appointment_score)

            # index of maximum of each list
            if complaint_max > threshold or complaint_max > threshold:
                if complaint_max > appointment_max:
                    sentiment = "complaint"
                else:
                    sentiment = "appointment"
            else:
                sentiment = "other"
            return Response({'success': 'Sentiment analysis completed successfully', 'sentiment': sentiment}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AutoRespond(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        data = request.data
        print(data)

        text = data['text']

        try:

            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            headers = {
                "Authorization": "Bearer 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"}

            def query(payload):
                response = requests.post(
                    API_URL, headers=headers, json=payload)
                return response.json()

            reply = query({
                "inputs": {
                    "past_user_inputs": ["who are you?"],
                    "generated_responses": ["I'm a customer service chatbot, how can I help you ?"],
                    "text": text,
                },
            })

            return Response({'success': 'Auto responded successfully',
                             'reply': reply['generated_text']}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def ActivateAccount(request, uid, token):
    user = request.user
    try:
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.profile.save()
        user.save()

        return redirect("https://orangewaves.tech/management/profile/settings")

    else:
        return redirect(website)


def RedirectToFrontEnd(request):
    user = request.user
    return redirect(website)


def googleVerification(request):
    return render(request, 'google26a07d368bac3722.html')


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
