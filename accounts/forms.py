from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.contrib.auth import authenticate


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class RegisterForm(forms.Form):
    email_form = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Email'
        }
    ))
    first_name_form = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your First Name'
        }
    ))
    last_name_form = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Last Name'
        }
    ))
    password_form = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Password'
        }
    ))
    confirm_password_form = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Your Password'
        }
    ))

    def clean_email_form(self):
        email = self.cleaned_data['email_form']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('this email is registered before')
        return email

    def clean_confirm_password_form(self):
        password = self.cleaned_data['password_form']
        confirm_password = self.cleaned_data['confirm_password_form']

        if password != confirm_password:
            raise forms.ValidationError('passwords must be same')
        return confirm_password


class LoginForm(forms.Form):
    email_form = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Email'
        }
    ))
    password_form = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Password'
        }
    ))

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email_form']
            password = self.cleaned_data['password_form']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('email or password is wrong')
