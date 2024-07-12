from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user'  ,'created', 'email_confirmed')
    list_filter = ('email_confirmed',)

    fieldsets = [

        ('Profile', {'fields': [('first_name', 'last_name'),
          ('email', 'avatar'),  'momentumPoints', ('username', 'user'),   'testsAttempted','email_confirmed', 'attempted']}),
    ]
    filter_horizontal = ('attempted',)

class SubjectAdmin(admin.ModelAdmin):
     list_display=('name',)
     fieldsets = [
             
            ('Subject', {'fields': ['name', 'topics']}),
     ]

     filter_horizontal = ('topics',)
        


class  PracticalAdmin(admin.ModelAdmin):
    
    fieldsets = [

        ('TestSeries', {'fields': ['name','image','information',  'subject', 'url']}),
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

class TestSeriesAdmin(admin.ModelAdmin):
    
    fieldsets = [

        ('TestSeries', {'fields': ['name','image','testInformation', 'tests']}),
    ]
    filter_horizontal=('tests',)   

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
class TestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    
    fieldsets = [

        ('Test', {'fields': ['name', 'question']}),
    ]
    filter_horizontal=   ('question',)

    







class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('id','level', 'subject')
    list_filter = ('category', 'level', 'subject')
    search_fields = ('answer', 'question')

    fieldsets =  [
         ('TestQuestion', {'fields': ['question', 'image', 'answer',     'options',('level', 'category'), ('subject', 'topic'), 'typeof'  ,'solutionVideo', 'correct_option']})
         
    ]
    



    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    











admin.site.register(Profile, ProfileAdmin)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(Subject,  SubjectAdmin)
admin.site.register(TestSeries  , TestSeriesAdmin)
admin.site.register(Topic)
admin.site.register(  PracticalSimulation,PracticalAdmin)
admin.site.register( Test, TestAdmin)












