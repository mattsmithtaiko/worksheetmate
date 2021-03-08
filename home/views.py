from django.shortcuts import render

from worksheets.forms import WorksheetForm

# Create your views here.
def index(request):
    add_worksheet_form = WorksheetForm()
    context = {'add_worksheet_form': add_worksheet_form,}
    return render(request, 'home/index.html', context)
