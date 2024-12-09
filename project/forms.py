from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class CustomUserCreationForm(UserCreationForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Group",
        widget=forms.Select
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'group')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
