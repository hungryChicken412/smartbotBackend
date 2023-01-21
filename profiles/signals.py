
import PIL.Image as Image
import numpy as np
import io
import json
import requests
import base64
from email.mime import base
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.dispatch import receiver
from .models import Profile
from django.core.files.storage import get_storage_class
import inspect
default_storage = get_storage_class()()


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name
        )
