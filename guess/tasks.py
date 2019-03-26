from __future__ import absolute_import, unicode_literals
from celery import shared_task
import subprocess
import csv
import argparse
from fastq_checker_pair import check_format_and_remove_low_quality_reads_pair
from fastq_checker_single import check_format_and_remove_low_quality_reads_single
from guesslib_single import guesslib_single
from guesslib_pair import guesslib_pair
from guesslib_genomic_pair import guesslib_genomic_pair
from .models import Result
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages


@shared_task
def guesslib_pair_task(user_email, domain, result_id, ref, forward_file_name, reverse_file_name, forward_file_path, reverse_file_path):
    '''Defining the algorithm as a task, saving the processed data and
     removes the upploaded files'''

    Result.objects.filter(pk=result_id).update(progress = 1)
    (libtype, outfwd, outrvs, inwfwd, inwrvs, collected_pairs,
     succesful_lib_determination, analysis_time) = guesslib_pair(
        ref, forward_file_name, reverse_file_name)
    if not libtype:
        subprocess.run(['rm', forward_file_path])
        subprocess.run(['rm', reverse_file_path])
    else:
        Result.objects.filter(pk=result_id).update(libtype=libtype, outfwd=outfwd, outrvs=outrvs, inwfwd=inwfwd, inwrvs=inwrvs, collected_pairs=collected_pairs, analysis_time=analysis_time)
        subprocess.run(['rm', forward_file_path])
        subprocess.run(['rm', reverse_file_path])
        result = Result.objects.get(pk=result_id)
        title = result.title
        date_submit = result.date_submit
        subject = str(title) + ' ' + str(date_submit)[0:10]
        from_email = 'GuessLib'
        to = str(user_email)
        html_message = render_to_string('guess/result_email_two.html', {'Result': Result.objects.get(pk=result_id), 'Domain': domain, })
        plain_message = strip_tags(html_message)
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    Result.objects.filter(pk=result_id).update(progress = 2)

@shared_task
def guesslib_single_task(user_email, domain, result_id, ref, reads_file_name, reads_file_path):
    '''Defining the algorithm as a task, saving the processed data and
     removes the upploaded files'''
    Result.objects.filter(pk=result_id).update(progress = 1)
    (libtype, inwfwd, inwrvs, collected_pairs,
     succesful_lib_determination, analysis_time) = guesslib_single(
        ref, reads_file_name)
    if not libtype:
        subprocess.run(['rm', reads_file_path])
    else:
        Result.objects.filter(pk=result_id).update(libtype=libtype, inwfwd=inwfwd, inwrvs=inwrvs, collected_pairs=collected_pairs, analysis_time=analysis_time)
        subprocess.run(['rm', reads_file_path])
        result = Result.objects.get(pk=result_id)
        title = result.title
        date_submit = result.date_submit
        subject = str(title) + ' ' + str(date_submit)[0:10]
        from_email = 'GuessLib'
        to = str(user_email)
        html_message = render_to_string('guess/result_email_one.html', {'Result': Result.objects.get(pk=result_id), 'Domain': domain, })
        plain_message = strip_tags(html_message)
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    Result.objects.filter(pk=result_id).update(progress = 2)
