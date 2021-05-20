from django import forms
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput())
    birth_date = forms.DateField(label='Birthday')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birth_date',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        min_length = 8

        if not password2:
            raise forms.ValidationError('You must confirm your password')
        if password1 != password2:
            raise forms.ValidationError('Your passwords do not match')
        if len(password1) < min_length:
            raise forms.ValidationError(f'Password must be at least {min_length} characters.')
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Password must contain at least 1 digit.')
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError('Password must contain at least 1 letter.')
        return password2

    def save(self, commit=True):
        new_user = super(UserCreationForm, self).save(commit=False)
        new_user.set_password(self.cleaned_data["password1"])
        if commit:
            new_user.save()
        return new_user


class QualitiesForm(forms.ModelForm):
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


class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(label='Birthday')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birth_date',)
