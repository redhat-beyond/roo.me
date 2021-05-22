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


class PreferencesSearchForm(forms.ModelForm):

    no_smoking = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'no-smoking',
                'value': 'no-smoking'
            }
        ),
        initial=False,
        required=False
    )

    pets_allowed = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'pets_allowed',
                'value': 'pets_allowed'
            }
        ),
        initial=False,
        required=False
    )

    air_conditioner = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'air-con',
                'value': 'air-con'
            }
        ),
        initial=False,
        required=False
    )

    balcony = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'balcony',
                'value': 'balcony'
            }
        ),
        initial=False,
        required=False
    )

    elevator = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'elevator',
                'value': 'elevator'
            }
        ),
        initial=False,
        required=False
    )

    long_term = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'long-term',
                'value': 'long-term'
            }
        ),
        initial=False,
        required=False
    )

    immediate_entry = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'immediate-entry',
                'value': 'immediate-entry'
            }
        ),
        initial=False,
        required=False
    )

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