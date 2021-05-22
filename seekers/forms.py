from django import forms
from .models import Seeker
from django.core.validators import MinValueValidator


class SeekerUpdateForm(forms.ModelForm):
    min_rent = forms.IntegerField(label='Minimum rent', validators=[MinValueValidator(limit_value=0)])
    max_rent = forms.IntegerField(label='Maximum rent', validators=[MinValueValidator(limit_value=0)])
    num_of_roomates = forms.IntegerField(label='Number of roomates', validators=[MinValueValidator(limit_value=0)])
    num_of_rooms = forms.IntegerField(label='Number of rooms', validators=[MinValueValidator(limit_value=0)])
    start_date = forms.DateField(label='Entry date [YYYY-MM-DD]')

    class Meta:
        model = Seeker
        fields = (
            'city',
            'start_date',
            'min_rent',
            'max_rent',
            'num_of_roomates',
            'num_of_rooms',
            'about',
        )

    def clean_max_rent(self):
        max_rent = self.cleaned_data.get('max_rent')
        min_rent = self.cleaned_data.get('min_rent')

        if not min_rent:
            raise forms.ValidationError('must have min rent')
        if not max_rent:
            raise forms.ValidationError('must have max rent')
        if max_rent < min_rent:
            raise forms.ValidationError('max rent must be larger than min rent')
        return max_rent


class SeekerCreationForm(SeekerUpdateForm):
    def save(self, commit=False):
        if commit:
            raise ValueError("Can't save to the data-base without owner field")
        else:
            new_seeker = super().save(commit=False)
            return new_seeker
