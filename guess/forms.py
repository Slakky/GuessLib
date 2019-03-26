from django import forms
from .models import Result, RefGenome
from django.conf import settings


class SubmitFileForm(forms.ModelForm):
    forward_file = forms.FileField()
    reverse_file = forms.FileField()

    class Meta:
        model = Result
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(SubmitFileForm, self).__init__(*args, **kwargs)
        self.fields['refgenome'] = forms.ModelChoiceField(queryset=RefGenome.objects.all(), empty_label='')


class SubmitOneFileForm(forms.ModelForm):
    reads = forms.FileField()

    class Meta:
        model = Result
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(SubmitOneFileForm, self).__init__(*args, **kwargs)
        self.fields['refgenome'] = forms.ModelChoiceField(queryset=RefGenome.objects.all(), empty_label='')


# class SubmitFileForm(forms.ModelForm): --> this way we can save fields of the form to the db (model)
#     title = forms.CharField(max_length=50)
#     file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
