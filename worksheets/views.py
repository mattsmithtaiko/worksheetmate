import subprocess
import os

from django.shortcuts import render, redirect
from django.http import FileResponse
from django.contrib import messages
from django.conf import settings

from .models import Worksheet
from questions.models import Question
from .forms import *

# Create your views here.
def index(request):
    if request.method == 'GET':
        search_form = SearchWorksheetsForm(request.GET)
        if search_form.is_valid() and search_form.cleaned_data['search_text'] != '':
            search_text = search_form.cleaned_data['search_text']
            worksheet_list = Worksheet.objects.filter(name__icontains=search_text) #The | represents set union
            worksheet_list = worksheet_list.distinct().order_by('name') #remove duplicate search results and order them
        else:
            worksheet_list = Worksheet.objects.all().order_by('name')
    else:
        worksheet_list = Worksheet.objects.all().order_by('name')

    if request.method == 'POST':
        add_worksheet_form = WorksheetForm(request.POST)
        if add_worksheet_form.is_valid():
            name = add_worksheet_form.cleaned_data['name']
            add_worksheet_form.save()
            messages.success(request, name + " added.")
        else:
            messages.error(request, "Something went wrong.")
    else:
        add_worksheet_form = WorksheetForm()

    search_form = SearchWorksheetsForm()
    search_form_placeholder = request.GET.get('search_text', 'Search')
    if search_form_placeholder == '':
        search_form_placeholder = 'Search'
    search_form.fields['search_text'].widget.attrs["placeholder"] = search_form_placeholder

    context = {
        'worksheet_list': worksheet_list,
        'search_form': search_form,
        'add_worksheet_form': add_worksheet_form,
    }
    return render(request, 'worksheets/list_of_worksheets.html', context)

def download(request, worksheet_pk):
    answer_str = '';
    show_answers = False
    download_source = False
    if request.method == 'GET':
        form = DownloadWorksheetForm(request.GET)
        if form.is_valid():
            option = form.cleaned_data['option']
            if option == 'answers':
                show_answers = True
                answer_str = '[answers]'
            elif option == 'source':
                download_source = True

    worksheet = Worksheet.objects.get(pk = worksheet_pk)
    block_set = worksheet.blocks_in_order()
    latex_file = open(settings.LATEX_FILES_ROOT + "/" + str(worksheet_pk) + answer_str + ".tex","w")
    latex_file.write(r'\documentclass{mcs5frmt}')
    latex_file.write("\n")
    latex_file.write(r'\usepackage' + answer_str + r'{mcs5gmt2}')
    latex_file.write("\n")
    latex_file.write(r'\usepackage{mcs5math}')
    latex_file.write("\n")
    latex_file.write(r'\settitle{' + worksheet.name + r'}')
    latex_file.write("\n")
    latex_file.write(r'\setcourse{' + worksheet.course.number + r'}')
    latex_file.write("\n")
    latex_file.write(r'\setdate[' + str(worksheet.date.year) + r']{' + str(worksheet.date.month) + r'}{' + str(worksheet.date.day) + r'}')
    latex_file.write("\n\n")
    latex_file.write(r'\begin{document}')
    latex_file.write("\n")
    #currently this code assumes that there will never be two consecutive direction blocks. If there are, you'll get a \begin{questions}\end{questions} and hence a missing \item error. Same error if a direction block is last.
    #really need to clean this up at some point -- might require rethinking direction blocks
    latex_file.write(r'  \begin{questions}')
    latex_file.write("\n")
    first_time = True
    for b in block_set:
        if first_time:
            if b.is_directionsblock():
                latex_file.write(b.worksheetformatblock.latex_code)
            first_time = False
        if b.is_singlequestion():
            latex_file.write(r'    \question{' + b.text + r'}{' + b.question.singlequestion.answer + r'}')
            latex_file.write("\n")
        elif b.is_multipartquestion():
            latex_file.write(r'    \questionwithparts{' + b.text + r'}{%')
            latex_file.write("\n")
            qparts = b.question.multipartquestion.questionpart_set.all().order_by("part_order")
            row_count = 0
            stretch_count = 0
            partnum_counter = 0
            for part in qparts:
                if partnum_counter == 0: #only increments counters once per row
                    row_count += 1
                    stretch_count += part.stretch_factor
                partnum_counter += 1
                if partnum_counter == part.num_per_row:
                    partnum_counter = 0
            latex_file.write(r'      \setstretchfactor{' + str(row_count) + r'}{' + str(stretch_count) + '}')
            latex_file.write("\n")
            for part in qparts:
                latex_file.write(r'      \qpart[' + str(part.num_per_row) + r']{' + str(part.stretch_factor) + r'}{' + part.text + r'}{' + part.answer + r'}')
                latex_file.write("\n")
            latex_file.write(r'}')
            latex_file.write("\n")
        elif b.is_worksheetformatblock():
            if not show_answers or b.is_directionsblock():
                latex_file.write(b.worksheetformatblock.latex_code)
                latex_file.write("\n")
    latex_file.write(r'  \end{questions}')
    latex_file.write("\n")
    latex_file.write(r'\end{document}')
    latex_file.close()
    if download_source:
        filename = settings.LATEX_FILES_ROOT + '/' + str(worksheet.pk) + '.tex'
        response = FileResponse(open(filename, "rb"), content_type='text/plain')
        response['Content-Disposition'] = 'filename="' + worksheet.name + '.tex"'
    else:
        error_file = open(settings.LATEX_FILES_ROOT + "/" + str(worksheet_pk) + "[errors].txt","w")
        my_env = os.environ.copy()
        my_env["PATH"] = "/usr/bin:" + settings.TEXLIVE_ROOT + ":"
        owd = os.getcwd() #original working directory
        os.chdir(settings.LATEX_FILES_ROOT)
        process = subprocess.run(['latexmk', '-pdf', '-cd', str(worksheet.pk) + answer_str + '.tex'], env=my_env)
        #process2 = subprocess.run(['latexmk', '-c'], env=my_env)
        error_file.close()
        os.chdir(owd)
        filename = settings.LATEX_FILES_ROOT + '/' + str(worksheet.pk) + answer_str + '.pdf'
        response = FileResponse(open(filename, "rb"), content_type='application/pdf')
        if show_answers:
            response['Content-Disposition'] = 'filename="' + worksheet.name + '[answers].pdf"'
        else:
            response['Content-Disposition'] = 'filename="' + worksheet.name + '.pdf"'
    return response

# def add(request):
#     if request.method == 'POST':
#         form = WorksheetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/worksheets/index')
#     else:
#         form = WorksheetForm()
#         context = {
#             'form': form,
#         }
#         return render(request, 'worksheets/add_worksheet.html', context)

def edit(request, worksheet_pk):
    worksheet = Worksheet.objects.get(pk=worksheet_pk)
    pagebreak_pk = WorksheetFormatBlock.objects.filter(latex_code=r'\newpage').get().pk
    extrawhitespace_pk = WorksheetFormatBlock.objects.filter(latex_code=r'\vfill').get().pk
    removewhitespace_pk = WorksheetFormatBlock.objects.filter(latex_code=r'\vspace{-\fill}\vspace{\baselineskip}').get().pk

    if request.method == 'POST':
        properties_form = WorksheetForm(request.POST, instance=worksheet, prefix="properties")
        directionsblock_form = DirectionsBlockForm(request.POST, prefix="directionsblock")
        if properties_form.is_valid():
            properties_form.save()
            messages.success(request, worksheet.name + " properties updated.")
        else:
            properties_form = WorksheetForm(instance=worksheet, prefix="properties")

        if directionsblock_form.is_valid():
            directionsblock_form.save()
            worksheet.blocks.add(directionsblock_form.instance)
            messages.success(request, "Direction block added.")
        else:
            directionsblock_form = DirectionsBlockForm(prefix="directionsblock")
    else:
        properties_form = WorksheetForm(instance=worksheet, prefix="properties")
        directionsblock_form = DirectionsBlockForm(prefix="directionsblock")

    num_of_questions = 0
    block_order = worksheet.block_order.split(';')
    block_list = []
    if worksheet.block_order != '':
        for block_pk in block_order:
            block = worksheet.blocks.get(pk=int(block_pk))
            block_list += [block]
            if block.is_question():
                num_of_questions += 1
    else:
        block_list = None

    context = {
        'worksheet': worksheet,
        'pagebreak_pk': pagebreak_pk,
        'extrawhitespace_pk': extrawhitespace_pk,
        'removewhitespace_pk': removewhitespace_pk,
        'block_list': block_list,
        'num_of_questions': num_of_questions,
        'properties_form': properties_form,
        'directionsblock_form': directionsblock_form,
    }
    return render(request, 'worksheets/edit_worksheet.html', context)

def remove(request, worksheet_pk):
    worksheet = Worksheet.objects.get(pk=worksheet_pk)
    worksheet.delete()
    return redirect('/worksheets/index')

#this method will allow for duplicate blocks, as opposed to adding them using the worksheet's default method
def add_worksheetformatblock(request, worksheet_pk, block_pk, index):
    worksheet = Worksheet.objects.get(pk=worksheet_pk)
    block = Block.objects.get(pk=block_pk)
    if worksheet.blocks.filter(pk=block_pk).exists():
        worksheet.add_block_to_order_after(block_pk, index)
        worksheet.save()
    else:
        worksheet.blocks.add(block) #add block to end (and in database)
        worksheet.swap_after(len(worksheet.get_split_block_order()) - 1, index)
        worksheet.save()
    return redirect('/worksheets/edit/' + str(worksheet_pk))

def swap_block(request, worksheet_pk, prev_or_next, block_index):
    worksheet = Worksheet.objects.get(pk=worksheet_pk)
    if prev_or_next == 'prev':
        worksheet.swap_with_previous(block_index)
    elif prev_or_next == 'next':
        worksheet.swap_with_next(block_index)
    worksheet.save()
    return redirect('/worksheets/edit/' + str(worksheet_pk))

def remove_block(request, worksheet_pk, block_index):
    worksheet = Worksheet.objects.get(pk=worksheet_pk)
    block = worksheet.blocks_in_order()[block_index]
    worksheet.remove_block_from_order(block_index)
    if not str(block.pk) in worksheet.block_order: #if that was the last instance, remove it from the relation
        worksheet.blocks.remove(block)
        if block.is_directionsblock(): #if removing a direction block, purge it from the database completely
            block.delete()
    worksheet.save()
    return redirect('/worksheets/edit/' + str(worksheet_pk))
