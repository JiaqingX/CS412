# mini_fb/admin.py

from django.contrib import admin
from .models import Profile, StatusMessage, Image

# Register the models to be visible in the Django admin interface
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
