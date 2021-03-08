from django import forms
from django.forms import modelform_factory, modelformset_factory

from .models import *
from worksheets.models import Worksheet

class QuestionForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset = Question.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )
    worksheet = forms.ModelChoiceField(
        queryset = Worksheet.objects.all(),
        empty_label = "Select a worksheet...",
    )

class SearchQuestionsForm(forms.Form):
    search_text = forms.CharField(required=False, label="")

class AddQuestionForm(forms.Form):
    choice = forms.ChoiceField(choices=[('SingleQuestion', 'Single Question'),('MultipartQuestion', 'Multipart Question')], widget=forms.RadioSelect)

AddSingleQuestionForm = modelform_factory(SingleQuestion, fields='__all__') #<--- work on this, then use formsets for the multipartquestion

AddMultipartQuestionForm = modelform_factory(MultipartQuestion, fields='__all__')
AddPartFormset = modelformset_factory(QuestionPart, exclude=("question", "part_order",))
