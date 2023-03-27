from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='password_confirmation', widget=forms.PasswordInput)
    join_clan = forms.BooleanField(label='Join the clan',
                                   required=True,
                                   error_messages={'required': "You must agree to join the clan"})

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password', 'join_clan')

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords don't match")
        return password_confirmation

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('There is an account connected with this email')
        return email

    def save(self, commit=True):
        user = get_user_model().objects.create_user(
            email=self.cleaned_data.get('email'),
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password'),
        )
        if commit:
            user.save()
        return user


class UserLogin(forms.Form):
    username = forms.CharField(label='username',
                               widget=forms.TextInput())
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
