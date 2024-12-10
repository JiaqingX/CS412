from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

# Custom user creation form to include a group selection field
class CustomUserCreationForm(UserCreationForm):
    # Adding a group selection field to the form
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),  # Queryset for all available groups
        required=True,  # Making the field mandatory
        label="Group",  # Label for the form field
        widget=forms.Select  # Using a dropdown select widget
    )

    class Meta:
        # Defining the model and fields for the form
        model = User
        fields = ('username', 'password1', 'password2', 'group')  # Fields to include in the form

    # Overriding the save method to handle the user creation process
    def save(self, commit=True):
        user = super().save(commit=False)  # Save the user object without committing to the database
        if commit:  # If commit is True, save the user object to the database
            user.save()
        return user


from django import forms
from .models import Enrollment

# Form for managing enrollments
class EnrollmentForm(forms.ModelForm):
    class Meta:
        # Defining the model and fields for the form
        model = Enrollment
        fields = ['student', 'course']  # Fields to include in the form


from django import forms
from .models import Attendance

# Form for managing attendance records
class AttendanceForm(forms.ModelForm):
    class Meta:
        # Defining the model and fields for the form
        model = Attendance
        fields = ['student', 'date', 'status']  # Fields to include in the form


from django import forms
from .models import Resource

# Form for managing resources
class ResourceForm(forms.ModelForm):
    class Meta:
        # Defining the model and fields for the form
        model = Resource
        fields = ['title', 'file', 'url']  # Fields to include in the form
