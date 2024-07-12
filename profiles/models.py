import inspect
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


def savenameLocation(self, filename):
    return f'userdata/{self.user.username}_files/{filename}'


def savenameLocationForCb(self, filename):
    return f'userdata/{self.parent.username}_files/{filename}'



typeOfCategory = (
    ('11', 'Numerical - Easy'),
    ('12', 'Numerical - Hard'),
    ('21', 'Theory - Easy'),
    ('22', 'Theory - Hard'),
)
questionCategory = (
     ('PYQ','Previous Year Exam Question'),
      ('MDL', 'Model Test Question'),

)
questionLevel = (
    ('E','Easy'),
    ('M','Medium'),
    ('H','Hard')
)




class Subject(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    topics = models.ManyToManyField('Topic', null=True, related_name="topics_subjects")


    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}"

class Test(models.Model):
    name = models.CharField(max_length=200)
    
    question = models.ManyToManyField('TestQuestion', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}--{self.created}"
class  PracticalSimulation(models.Model):
    name = models.CharField(max_length=200)
    
    
    created = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    information = models.TextField()
    url = models.CharField(max_length=200)


    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}--{self.created}"




    

class TestSeries(models.Model):
    name = models.CharField(max_length=200)
    
    tests = models.ManyToManyField('Test', null=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    testInformation = models.TextField()


    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}"


class Topic(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}"

class TestQuestion(models.Model):
     
    question = models.TextField(max_length=200)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    answer = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    level = models.CharField(max_length=200, choices= questionLevel, default='E')

    category = models.CharField(max_length=3, choices=questionCategory, default='PYQ')
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, null=True) 
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, null=True)
    typeof = models.CharField(max_length=200,  choices=typeOfCategory, default='11')

    options = models.CharField(max_length=200)
    solutionVideo = models.CharField(max_length=200, null=True, blank=True)
    correct_option = models.CharField(max_length=200)

    

    

    def __str__(self):
        return f"{self.question}"
class Profile(models.Model):

    ## BASE ##

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    email = models.EmailField(max_length=200)
    avatar = models.ImageField(
        default='avatars/chicken.jpg', upload_to=savenameLocation)
    username = models.CharField(max_length=200, default='#user')
    momentumPoints = models.IntegerField(default=0)
    testsAttempted = models.ManyToManyField(Test, null=True)

    

    

    created = models.DateTimeField(auto_now_add=True)
    attempted = models.ManyToManyField(TestQuestion, null=True,related_name="attemptedQuestions_profiles" )
    bookmarked = models.ManyToManyField(TestQuestion, null=True,related_name="bookmarkedQuestions_profiles"  )
    # SubscriptionPlan = models.ManyToManyField(SubscriptionPlan, on_delete=models.PROTECT , default=1)

    ## END_BASE ##

    ## ACTIVITY / STATS ##
    email_confirmed = models.BooleanField(default=False)

    ## END_ACTIVITY / END_STATS ##

    @property
    def user__username(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return f"{self.user.username}---{self.created}"

