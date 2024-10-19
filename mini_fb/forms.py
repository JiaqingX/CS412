# mini_fb/forms.py

from django import forms
from .models import Profile

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']

from .models import StatusMessage

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']

from django import forms
from .models import Profile

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'email', 'profile_image_url']

