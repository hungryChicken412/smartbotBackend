import inspect
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def savenameLocation(self, filename):
    return f'userdata/{self.user.username}_files/{filename}'


def savenameLocationForCb(self, filename):
    return f'userdata/{self.parent.username}_files/{filename}'


bot_status = [

    ('Development', 'Development'),
    ('Online', 'Online'),
    ('Offline', 'Offline'),
    ('Error', 'Error')

]
helpdeskTicket_status = [
    ('Pending', 'Pending'),
    ('Resolved', 'Resolved'),
]


class Profile(models.Model):

    ## BASE ##

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    email = models.EmailField(max_length=200)
    avatar = models.ImageField(
        default='avatars/chicken.jpg', upload_to=savenameLocation)
    username = models.CharField(max_length=200, default='#user')
    companyUrl = models.CharField(max_length=200, default='#companyUrl')

    created = models.DateTimeField(auto_now_add=True)
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
        return f"{self.user.username}--{self.companyUrl}--{self.created}"


class AnalyticsLog(models.Model):
    time = models. DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(default=None)
    user_meta = models.TextField(default='')

    def __str__(self):
        return str(self.time.strftime("%H:%M:%S")) + " @ "+self.user_ip


class IssueTicket(models.Model):
    time = models. DateTimeField(auto_now_add=True)
    logs = models.TextField(default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=20, choices=helpdeskTicket_status, default='Pending')
    bot = models.ForeignKey('Chatbot', on_delete=models.CASCADE)
    ticketID = models.CharField(max_length=20, default="")

    def __str__(self):
        return str(self.ticketID + " @ "+self.state)


class Chatbot(models.Model):
    name = models.CharField(max_length=300)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    chatbotData = models.TextField(default='')
    chatbotHostData = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    website = models.URLField(blank=True)
    avatar = models.FileField(
        default='avatars/chicken.jpg', upload_to=savenameLocationForCb)
    caching = models.BooleanField(default=False)
    tokenID = models.CharField(max_length=300, default="")
    article = models.TextField(default='')

    # Analytics
    logs = models.ManyToManyField(
        AnalyticsLog,   blank=True)
    status = models.CharField(
        max_length=20, choices=bot_status, default='Development')

    def __str__(self):
        return self.parent.username + ' - ' + self.name
