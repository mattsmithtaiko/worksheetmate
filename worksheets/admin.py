from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Worksheet)
admin.site.register(Course)
admin.site.register(WorksheetFormatBlock)
admin.site.register(WFBDirections)
