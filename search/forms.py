from django import forms
from seekers.models import Seeker
from django.core.validators import MinValueValidator    


class SearchForm(forms.ModelForm):
    min_rent = forms.IntegerField(label='Minimum rent', validators=[MinValueValidator(limit_value=0)])
    max_rent = forms.IntegerField(label='Maximum rent', validators=[MinValueValidator(limit_value=0)])
    num_of_roomates = forms.IntegerField(label='Number of roomates', validators=[MinValueValidator(limit_value=0)])
    num_of_rooms = forms.IntegerField(label='Number of rooms', validators=[MinValueValidator(limit_value=0)])
    start_date = forms.DateField(label='Start date [YYYY-MM-DD]')

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
