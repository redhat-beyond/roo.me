from django import forms
from seekers.models import Seeker
from django.core.validators import MinValueValidator
from users.models import User


class SearchForm(forms.ModelForm):
    min_rent = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'type': 'number',
                'class': 'form-control',
                'id': 'min-rent',
            }
        ),
        validators=[MinValueValidator(limit_value=0)]
    )

    max_rent = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
               'type': 'number',
                'class': 'form-control',
                'id': 'max-rent',
            }
        ),
        validators=[MinValueValidator(limit_value=0)]
    )
    
    num_of_roomates = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
               'type': 'number',
                'class': 'form-control',
                'id': 'roommates', 
            }
        ),
        validators=[MinValueValidator(limit_value=0)]
    )

    num_of_rooms = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
               'type': 'number',
                'class': 'form-control',
                'id': 'num_rooms',
            }
        ),
        validators=[MinValueValidator(limit_value=0)]
    )

    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
               'type': 'date',
                'class': 'form-control',
                'id': 'start-date', 
            }
        )
    )

    no_smoking = forms.MultipleChoiceField

    class Meta:
        model = Seeker
        fields = [
            'city',
            'start_date',
            'min_rent',
            'max_rent',
            'num_of_roomates',
            'num_of_rooms',
        ]

class PreferenceSearchForm(forms.ModelForm):

    no_smoking = forms.BooleanField()
    pet_friendly = forms.BooleanField()
    air_conditioner = forms.BooleanField()
    balcony = forms.BooleanField()
    elevator = forms.BooleanField()
    long_term = forms.BooleanField()
    immediate_entry = forms.BooleanField()

    class Meta:
        model = User
        fields = [
            'not_smoking',
            'pets_allowed',
            'air_conditioner',
            'balcony',
            'elevator',
            'long_term',
            'immediate_entry'
        ]