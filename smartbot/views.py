

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
from django.core.paginator import Paginator

import sys 
sys.path.append("..") 
from blog.models import BlogPost
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
                        
                        #user.email_user(subject, message)
                        

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


class Analysis(APIView):
    permission_classes = (permissions.AllowAny,)
    

    
    def analyze_data(self, data):
        print(data)
        efficiency = 0;##(data['timetaken']) / data['totalTime']
        
        subject_analysis = self.analyze_subjects(data['subjectWise'])
        totalCorrectEfficiency = data['correct'] / data['totalQuestions']
        suggestions = []
        if(totalCorrectEfficiency < 0.5):
            suggestions = ["You need to revise everything, you got less than 50% correct."]
        elif totalCorrectEfficiency < 0.7:
            suggestions = ["You need to revise more, you got less than 70% correct."]
        elif totalCorrectEfficiency < 0.8:
            suggestions = ["You did good!"]
        elif totalCorrectEfficiency >= 0.9:
            suggestions = ["You did great! more than 90% correct!"]

        
        

        
        if efficiency > 0.9:
            suggestions.append("Time management could be improved.")
        else:
            suggestions.append("Good time management. Keep it up!")

        suggestions.extend(self.generate_suggestions(data, subject_analysis))
        ## create a point system, so score is calculated based on the data
        
            # Point system
        EfficiencyWeight = 50
        CorrectnessWeight = 50
        SubjectWeight = 10
        TimeManagementWeight = -10  # Deduct points for poor time management
        BonusWeight = 5


        
        # Calculate efficiency score
        efficiencyScore = (1 - efficiency) * EfficiencyWeight if data['totalTime'] > 0 else 0
        # Calculate correctness score
        correctnessScore = (totalCorrectEfficiency * CorrectnessWeight)
        # Calculate subject analysis score
        subjectScore = sum([analysis['correctRatio'] * SubjectWeight for subject, analysis in subject_analysis.items()])
        # Calculate time management score
        timeManagementScore = (data['longestQuestionTime'] - 60) * TimeManagementWeight if data['longestQuestionTime'] > 60 else 0
        # Calculate bonus points
        bonusPoints = (60 - data['shortestQuestionTime']) * BonusWeight if data['shortestQuestionTime'] < 60 else 0

        
        # Total momentum points
        momentumPoints = efficiencyScore + correctnessScore + subjectScore + timeManagementScore #+ bonusPoints
        momentumPoints = round(momentumPoints*data['totalQuestions'], 2)
        suggestions.append(f"Your total momentum points are {momentumPoints}")
        #suggestions.append(f"The score near 100 is good, the higher the better, the score near 0 is bad, the lower the worse.")
        air = 20000

        finalResult = {
            'efficiency': efficiency,
            'totalCorrectEfficiency': totalCorrectEfficiency,
            'subjectAnalysis': subject_analysis,
            'momentumPoints': momentumPoints,
            'subjectToImprove': min(subject_analysis, key=lambda x: subject_analysis[x]['correctRatio']),
            'topicToImprove': min(subject_analysis[min(subject_analysis, key=lambda x: subject_analysis[x]['correctRatio'])], key=lambda x: subject_analysis[max(subject_analysis, key=lambda x: subject_analysis[x]['correctRatio'])][x]),
            'strongestSubject': max(subject_analysis, key=lambda x: subject_analysis[x]['correctRatio']),   
            'strongestTopic': max(subject_analysis[max(subject_analysis, key=lambda x: subject_analysis[x]['correctRatio'])], key=lambda x: subject_analysis[max(subject_analysis, key=lambda x: subject_analysis[x]['correctRatio'])][x]),




            'scores':{
                'efficiencyScore': efficiencyScore,
                'correctnessScore': correctnessScore,
                'subjectScore': subjectScore,
                'timeManagementScore': timeManagementScore,
                'bonusPoints': bonusPoints
            },
            'AIR':air,    
            

            'suggestions': suggestions
        }
        self.request.user.profile.momentumPoints += momentumPoints
        
        for q in data['attemptedQuestionIDs']:
            if self.request.user.profile.attempted.filter(id=q).exists():
                pass
            else:
                self.request.user.profile.attempted.add(q)

        

        

        self.request.user.profile.save()

        return  finalResult

    def analyze_subjects(self, subjects):
        subject_analysis = {}
        for subject, details in subjects.items():
            for topic, stats in details.items():
                correct_ratio = stats['correct'] / stats['totalQuestions'] if stats['totalQuestions'] > 0 else 0
                time_per_question = stats['timeSpent'] / stats['totalQuestions'] if stats['totalQuestions'] > 0 else 0
                subject_analysis[topic] = {
                    'correctRatio': correct_ratio,
                    'timePerQuestion': time_per_question,
                    'totalQuestions': stats['totalQuestions'],
                }
        return subject_analysis

    def generate_suggestions(self, data, subject_analysis):
        suggestions = []
        for subject, analysis in subject_analysis.items():
            if(analysis['totalQuestions'] > 0):
                suggestions.append(f"Analysis for {subject}:")
                if analysis['correctRatio'] < 0.5:
                    suggestions.append(f"Consider revising {subject}, as the correctness ratio is low. You got {analysis['correctRatio']} correct per question.")
                if analysis['timePerQuestion'] > 60:  # Assuming 60 seconds is the expected average
                    suggestions.append(f"Improve time management in {subject}. The average time spent on a question is {analysis['timePerQuestion']} seconds.")

            
                
            
        suggestions.append(f"The longest you spent your time was on Question No {data['longestQuestionID'] + 1} which was {data['longestQuestionTime']} seconds or {data['longestQuestionTime']/60} minutes.")
        
        if(data['longestQuestionTime']) > 60:
            suggestions.append(f"Consider reducing this time spent, as it is significantly higher than the average time spent on a question. You wasted {data['longestQuestionTime'] - 60} seconds on this question")

            if (data['questionWise'][str(data['longestQuestionID'])]['correct'] != True):
                suggestions.append(f"Also, you got this question wrong, consider revising this topic, in exam consider leaving these type of questions which you are not sure about.")
                    
            else:
                suggestions.append(f"you got this question right, consider reducing the time spent on this question. More practice is needed for you!.")
        else:
            suggestions.append(f"the longest time you spent on a question was {data['longestQuestionTime']} seconds, which is good as it is lesser than the average.")
            
            
            
            if (data['questionWise'][str(data['longestQuestionID'])]['correct']  != True):
                    suggestions.append(f"However, you got this question wrong, consider revising this topic, please revise and check what went wrong.")
            else:
                    suggestions.append(f"Plus you got it right! Very good!.")
            
        suggestions.append(f"the shortest time you spent on a question was on Q.{int(data['shortestQuestionID']) + 1} which was {data['shortestQuestionTime']} seconds.")
        if(data['shortestQuestionTime']) > 60:
            suggestions.append(f"You're wasting a lot of time, the average time should be 60s/question, and the shortest you take on a question should be about 40-50s, you're taking more than 50.")
            if (data['questionWise'][str(data['shortestQuestionID'])]['correct']   != True):
                suggestions.append(f"Also, you got this question wrong, consider revising this topic, in exam consider leaving these type of questions which you are not sure about.")
            else:
                suggestions.append(f"you got this question right, but still, please reduce the time taken.")
        elif  (data['shortestQuestionTime']) == 0:
            pass
        else:
            if (data['questionWise'][str(data['shortestQuestionID'])]['correct']  != True):
                suggestions.append(f"However, you got this question wrong, please revise.")
            else:
                suggestions.append(f"Plus you got it right! Very good!.")
            
            




                



                    


                


            
            
            
        
            

        return suggestions
    def post(self, request):

        data = request.data
        analysis = self.analyze_data(data)
        
        return Response({ 'status': 'success', 'analysis':analysis, }, status=status.HTTP_200_OK)


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


def LandingPage(request):
    return render(request, 'index.html')
def BlogPage(request, pk):
    
    blogs = BlogPost.objects.all().order_by('-published')
    paginator = Paginator(blogs, 8)  # Show 25 contacts per page.

    page_number = pk
    
    if page_number > paginator.num_pages:
        return redirect('https://localhost:8000/blogs/'  + str(paginator.num_pages)+"/")
    blogss = paginator.get_page(page_number)
    nextPage = int(pk)+1
    prevPage = int(pk)-1
    if nextPage > paginator.num_pages:
        nextPage = 0
    if prevPage < 1:
        prevPage = 0
    
    
    

    return render(request, 'blogList.html', {'blogs': blogss, 'nextPage':  nextPage, 'prevPage':  prevPage})
def BlogDetail(request, pk):
    print("here")
    blog =  BlogPost.objects.get(pk=pk)
     # new blogs 4
    blogs = BlogPost.objects.all().order_by('-published')
    if len(blogs) > 4:
        blogs = blogs[:4]
    else:
        pass

    return render(request, 'blog.html', {'blog': blog, 'blogs':blogs})
    

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
