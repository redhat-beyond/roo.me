from django import forms
from seekers.models import Seeker
from django.core.validators import MinValueValidator


class SearchForm(forms.ModelForm):
    min_rent = forms.IntegerField(validators=[MinValueValidator(limit_value=0)])
    max_rent = forms.IntegerField(validators=[MinValueValidator(limit_value=0)])
    num_of_roomates = forms.IntegerField(validators=[MinValueValidator(limit_value=0)])
    num_of_rooms = forms.IntegerField(validators=[MinValueValidator(limit_value=0)])

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
