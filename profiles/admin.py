from django.contrib import admin
from .models import *
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'companyUrl', 'created', 'email_confirmed')
    list_filter = ('email_confirmed',)

    fieldsets = [

        ('Profile', {'fields': ['first_name', 'last_name',
         'email', 'avatar', 'username', 'companyUrl', 'email_confirmed', 'user']}),
    ]


admin.site.register(Profile, ProfileAdmin)


admin.site.register(AnalyticsLog)
admin.site.register(Chatbot)


admin.site.register(IssueTicket)
