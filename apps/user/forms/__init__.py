from django import forms

from apps.user.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class CustomUserCreationForm(forms.ModelForm):
    password_one = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_two = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'phone_number',)

    def clean_password2(self):
        # Check that the two password entries match
        password_one = self.cleaned_data.get("password_one")
        password_two = self.cleaned_data.get("password_two")
        if password_one and password_two and password_one != password_two:
            raise forms.ValidationError("Passwords don't match")
        return password_two

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password_one"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'is_active', 'phone_number')

    def clean_password(self):
        return self.initial["password"]
