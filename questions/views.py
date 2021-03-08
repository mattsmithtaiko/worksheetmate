import subprocess
import os
import time

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models.query import QuerySet

from .models import *
from .forms import *
# Create your views here.
def index(request):
    if request.method == 'GET':
        search_form = SearchQuestionsForm(request.GET)
        if search_form.is_valid() and search_form.cleaned_data['search_text'] != '':
            search_text = search_form.cleaned_data['search_text']
            if search_text == 'unused': #special search term used to find unused questions
                question_list = Question.objects.filter(worksheet = None)
            else:
                question_list = Question.objects.filter(category__name__icontains=search_text) | Question.objects.filter(tags__name__icontains=search_text) | Question.objects.filter(worksheet__name__icontains=search_text) #The | represents set union
            question_list = question_list.distinct().order_by("-category") #remove duplicate search results and order them
        else:
            question_list = Question.objects.all().order_by("-category")
    else:
        question_list = Question.objects.all().order_by("-category")

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            choice_set = form.cleaned_data['choices'].all()
            worksheet = form.cleaned_data['worksheet']
            for choice in choice_set:
                worksheet.blocks.add(choice)
            messages.success(request, "Question added to " + worksheet.name)
        else:
            messages.error(request, "Something went wrong.")
    else:
        form = QuestionForm()

    search_form = SearchQuestionsForm()
    search_form_placeholder = request.GET.get('search_text', 'Search')
    if search_form_placeholder == '':
        search_form_placeholder = 'Search'
    search_form.fields['search_text'].widget.attrs["placeholder"] = search_form_placeholder
    context = {
        'question_list': question_list,
        'form': form,
        'search_form': search_form,
        }
    return render(request, 'questions/list_of_questions.html', context)

def add(request):
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            new_request = HttpRequest() #need to pass a new request so old POST data doesn't go through
            if choice == 'SingleQuestion':
                new_request = HttpRequest()
                return add_singlequestion(new_request)
            else:
                return add_multipartquestion(new_request)

    context = {
        'form': AddQuestionForm(),
        'formset': None,
        'form_action': 'add',
    }
    return render(request, 'questions/add_question.html', context)

def add_singlequestion(request):
    if request.method == 'POST':
        form = AddSingleQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New question added.")
        else:
            messages.error(request, "Something went wrong.")

        new_request = HttpRequest()
        return add(new_request)

    context = {
        'form': AddSingleQuestionForm(),
        'formset': None,
        'form_action': 'add/single',
    }
    return render(request, 'questions/add_question.html', context)

def add_multipartquestion(request):
    if request.method == 'POST':
        form = AddMultipartQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New question added.")
        else:
            messages.error(request, "Something went wrong.")

        new_request = HttpRequest()
        return add(new_request)

    form = AddMultipartQuestionForm()
    formset = AddPartFormset(queryset=QuestionPart.objects.none())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'questions/add_question.html', context)

def search_category(request):
    if request.method == "GET":
        search_text = request.GET['search_text']
        if search_text is not None and search_text != u"":
            search_text = request.GET['search_text']
            catsearch = Question.objects.filter(category__contains = search_text)
        else:
            catsearch = []

        return render(request, 'ajax_search.html', {'catsearch': catsearch})
