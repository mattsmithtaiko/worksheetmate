from django import forms
from django.forms import modelform_factory

from .models import *

class WorksheetForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset = Course.objects.all(),
        empty_label = None,
    )

    class Meta:
        model = Worksheet
        exclude = ["blocks", "block_order"]

DirectionsBlockForm = modelform_factory(WFBDirections, fields=("directions",))

class DownloadWorksheetForm(forms.Form):
    option = forms.CharField()

class SearchWorksheetsForm(forms.Form):
    search_text = forms.CharField(required=False, label="")
# class WorksheetForm(forms.Form):
#     worksheet_pk = forms.IntegerField(widget=forms.HiddenInput())
#
# class AddWorksheetForm(forms.Form):
#     name = forms.CharField()
#     description = forms.CharField(required=False)
#     date = forms.DateField()
#     course = forms.ModelChoiceField(
#         queryset = Course.objects.all(),
#         initial = 0,
#     )
#
# class WorksheetPropertyForm(forms.Form):
