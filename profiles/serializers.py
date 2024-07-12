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
            

        ]

class TestSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSeries
        fields = [
            'name', 'testInformation','image','tests', 'id']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rp = {}
        rp['name'] = representation['name']
        rp['id'] = instance.id
        rp['testInformation'] = representation['testInformation']
        rp['image'] = representation['image']
        rp['tests'] = []
        for test in representation['tests']:
            rp['tests'].append({ 'name':Test.objects.get(id=test).name, 
                                'id':Test.objects.get(id=test).id, 
                                'attempted':   self.context['request'].user.profile.testsAttempted.filter(id=test).exists()})

        return rp

        

class practicalSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PracticalSimulation
        fields = [
            'name', 'information','image','subject', 'id']
            

            

class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = [
            'question','image','answer','category','subject','correct_option','topic', 'solutionVideo','options'
            
        ]
    
    
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        
        rp = {}
        rp['question'] = representation['question']
        rp['img'] = representation['image']
        rp['correct'] = representation['correct_option']
        rp['solution'] = representation['answer']
        rp['solutionVideo'] =  representation['solutionVideo']
        rp['userAnswer'] = ''
        rp['options'] = representation['options']
        rp['id'] = instance.id
        rp['options'] = rp['options'].split('|')
        rp['subject']  = representation['subject']
        rp['topic'] = representation['topic']


        return rp

class  SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Subject
        fields = [
            'name', 'topics'
            
        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rp = {}
        rp['name'] = representation['name']
        rp['id'] = instance.id
        rp['topics'] = []
        for topic in representation['topics']:
            rp['topics'].append({ 'name':Topic.objects.get(id=topic).name, 'id':Topic.objects.get(id=topic).id})

        return rp


class ProfileMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'username',
            'avatar',
            'email',
            'momentumPoints',
            'testsAttempted',
            'attempted',
            'bookmarked'


        ]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rp = {}
        rp['username'] = representation['username']
        rp['avatar'] = representation['avatar']
        rp['email'] = representation['email']
        rp['momentumPoints'] = representation['momentumPoints']
        rp['testsAttempted'] =  instance.testsAttempted.count()
        rp['attempted'] = instance.attempted.count()
        rp['bookmarked'] =  instance.bookmarked. count()

        
        return rp
    



class ProfileEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
              'created', 'email_confirmed']
