import shlex
import subprocess
import os
import datetime
import sys
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import SubmitFileForm, SubmitOneFileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Result, RefGenome
from fastq_checker_pair import check_format_and_remove_low_quality_reads_pair
from fastq_checker_single import check_format_and_remove_low_quality_reads_single
from guesslib_single import guesslib_single
from guesslib_pair import guesslib_pair
from random import randint
from django.conf import settings
from django.shortcuts import render, redirect
from .tasks import guesslib_single_task, guesslib_pair_task

upload_dir = settings.BASE_DIR + '/tmp/'

def home(request):
    context = {
    }
    return render(request, 'guess/home.html', context)


def about(request):
    return render(request, 'guess/about.html', {'title': 'About'})


@login_required
def submit_one(request):
    user_object = User.objects.get(username=request.user)
    user_email = user_object.email
    domain = request.META['HTTP_HOST']
    context = {}
    if request.method == 'POST':
        submited_form = SubmitOneFileForm(request.POST, request.FILES)
        rand_str = randint(000000, 999999)
        reads = request.FILES['reads']
        reads_file_name = reads.name + str(request.user) + str(rand_str)
        reads_file_path = upload_dir + reads_file_name
        if submited_form.is_valid() and request.user.is_authenticated:
            form = submited_form.save(commit=False)
            form.author = request.user
            form.refgenome = submited_form.cleaned_data['refgenome']
            form.single = True
            fs = FileSystemStorage(location=upload_dir)
            fs.save(reads_file_name, reads)
            (proper_formats, form.nr_of_seqs_fout, form.fout_avg_quality,
                form.fin_avg_quality) = check_format_and_remove_low_quality_reads_single(reads_file_path)
            form.save()
            if proper_formats:
                refobject = RefGenome.objects.get(name=form.refgenome)
                ref = refobject.path
                guesslib_single_task.delay(user_email, domain, form.pk, ref, reads_file_name, reads_file_path)
                messages.success(request, f"Grab a coffee! Your job is being processed. An email will be sent to your address once it's done")
                return(redirect('guess-submit_one'))
            else:
                messages.warning(request, f'It seems like your file does not have the proper format. Please check your formatting.')
                subprocess.run(['rm', reads_file_name])
                return(redirect('guess-submit_one'))

            # return HttpResponseRedirect(reverse('result-detail', kwargs={'pk': form.pk}))
    else:
        submited_form = SubmitOneFileForm()
    context = {
        'submited_form': submited_form,
        'title': 'Submit job',
    }
    return render(request, 'guess/submit_one.html', context)


@login_required
def submit(request):
    user_object = User.objects.get(username=request.user)
    user_email = user_object.email
    domain = request.META['HTTP_HOST']
    context = {}
    if request.method == 'POST':
        submited_form = SubmitFileForm(request.POST, request.FILES)
        rand_str = randint(000000, 999999)
        forward_file = request.FILES['forward_file']
        forward_file_name = forward_file.name + str(request.user) + str(rand_str)
        forward_file_path = upload_dir + forward_file_name
        reverse_file = request.FILES['reverse_file']
        reverse_file_name = reverse_file.name + str(request.user) + str(rand_str)
        reverse_file_path = upload_dir + reverse_file_name
        if submited_form.is_valid() and request.user.is_authenticated:
            form = submited_form.save(commit=False)  # not commiting the form but creating the object
            form.author = request.user
            form.refgenome = submited_form.cleaned_data['refgenome']
            form.single = False
            fs = FileSystemStorage(location=upload_dir)
            fs.save(forward_file_name, forward_file)
            fs = FileSystemStorage(location=upload_dir)
            fs.save(reverse_file_name, reverse_file)
            (proper_formats, form.nr_of_seqs_fout, form.fout_avg_quality,
                form.fin_avg_quality) = check_format_and_remove_low_quality_reads_pair(forward_file_path, reverse_file_path)
            form.save()
            if proper_formats:
                refobject = RefGenome.objects.get(name=form.refgenome)
                ref = refobject.path
                guesslib_pair_task.delay(user_email, domain, form.pk, ref, forward_file_name, reverse_file_name, forward_file_path, reverse_file_path)
                messages.success(request, f"Grab a coffee! Your job is being processed. An email will be sent to your address once it's done")
                return(redirect('guess-submit'))
            else:
                messages.warning(request, f'It seems like your files do not have the proper format. Please check your formatting.')
                subprocess.run(['rm', forward_file_path])
                subprocess.run(['rm', reverse_file_path])
                return(redirect('guess-submit'))

            # return HttpResponseRedirect(reverse('result-detail', kwargs={'pk': form.pk}))

    else:
        submited_form = SubmitFileForm()
    context = {
        'submited_form': submited_form,
        'title': 'Submit job',
    }
    return render(request, 'guess/submit.html', context)


class ResultListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = 'guess/history.html'
    context_object_name = 'results'
    ordering = ['-date_submit']

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class ResultDetailView(LoginRequiredMixin, DetailView):
    model = Result
