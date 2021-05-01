from django import forms
from users.models import User
from .models import Apartment


class ApartmentDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'date_posted',
            'city',
            'address',
            'rent',
            'num_of_roomates',
            'num_of_rooms',
            'start_date',
            'about',
            'is_relevant',
            'image_url'
            ]


class ApartmentQualitiesUpdateForm(forms.ModelForm):
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
