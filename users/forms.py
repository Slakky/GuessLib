from django import forms
from django.contrib.auth.forms import User
from django_registration.forms import RegistrationFormUniqueEmail
from captcha.fields import ReCaptchaField


<<<<<<< HEAD
=======

>>>>>>> f54b90092c6a6fb9f26da8faad07ddf5460a4828
class RecaptchaRegistrationForm(RegistrationFormUniqueEmail):
    captcha = ReCaptchaField()


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
