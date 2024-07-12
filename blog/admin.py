from django.contrib import admin
from .models import *


class BlogPostAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Title/date", {'fields': ["title", "published"]}),
        ("Content", {"fields": ["content", "brief"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(BlogPost, BlogPostAdmin)

# Register your models here.
