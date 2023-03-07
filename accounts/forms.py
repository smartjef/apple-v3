from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, ResidentialInfo


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get("email", None)
        if email:
            if not User.objects.filter(email=email):
                return email
            else:
                raise forms.ValidationError('Email already taken')
        raise forms.ValidationError('Email field is required')


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserEditFormView(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'disabled': True}),
            'last_name': forms.TextInput(attrs={'disabled': True}),
            'email': forms.EmailInput(attrs={'disabled': True})
        }


class ProfileEditFormView(forms.ModelForm):  # for disabled fields
    class Meta:
        model = UserProfile
        fields = ('image', 'phone', 'description')
        widgets = {
            'phone': forms.TextInput(attrs={'disabled': True}),
            'description': forms.Textarea(attrs={'disabled': True, 'rows': 5})
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'phone', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5})
        }


class ResidentialInfoForm(forms.ModelForm):
    address = forms.CharField(required=True, help_text="e.g 20200 Juja")
    city = forms.CharField(required=True, help_text="e.g Nairobi")

    class Meta:
        fields = "__all__"
        exclude = ('user',)
        model = ResidentialInfo


class UserProfileInfo(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone',)


class ChangeProfilePicForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
