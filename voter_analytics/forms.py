# voter_analytics/forms.py
from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(
        choices=[(choice, choice) for choice in Voter.objects.values_list('party_affiliation', flat=True).distinct()],
        required=False
    )
    voter_score = forms.ChoiceField(
        choices=[(i, i) for i in range(6)],
        required=False
    )
