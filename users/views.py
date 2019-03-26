from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ContactForm
from GuessLib import urls
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from guess.models import Result
from django.contrib.auth.models import User
from GuessLib import settings
import json
import urllib.request
import urllib.parse
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             ''' Begin reCAPTCHA validation '''
#             recaptcha_response = request.POST.get('g-recaptcha-response')
#             url = 'https://www.google.com/recaptcha/api/siteverify'
#             values = {
#                 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
#                 'response': recaptcha_response
#             }
#             data = urllib.parse.urlencode(values).encode()
#             req = urllib.request.Request(url, data=data)
#             response = urllib.request.urlopen(req)
#             result = json.loads(response.read().decode())
#             ''' End reCAPTCHA validation '''
#             if result['success']:
#                 form.save()
#                 username = form.cleaned_data.get('username')
#                 raw_password = form.cleaned_data.get('password1')
#                 messages.success(request, f'Your account has been created! You are now able to log in')
#                 return redirect('login')
#             else:
#                 messages.error(request, f'Invalid reCAPTCHA. Please try again')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/registration_form.html', {'form': form, 'title': 'Register'})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'title': 'Profile'
    }
    return render(request, 'users/profile.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            msg_mail = str(message) + "\n" + "Sent from: " + str(email)
            try:
                send_mail(subject, msg_mail, email, ['guesslib@gmail.com'])
            except BadHeaderError:
                messages.warning(request, f'Invalid header found! Please try again')
                return redirect('contact')
            messages.success(request, f'We will contact you as soon as possible')
            return redirect('guess-home')
    else:
        form = ContactForm()
    return render(request, 'users/contact.html', {'form': form})

# @login_required
# def history(request):
#     user = request.user
#     print(user)
#     result = Result.objects.filter(author=request.user).order_by('-date_submit')
#     print(result)
#     return render(request, 'users/history.html', {'results': result})
