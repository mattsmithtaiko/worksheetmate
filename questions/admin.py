from django.contrib import admin

from .models import *
# Register your models here.

class SingleQuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

class QuestionPartInline(admin.TabularInline):
    model = QuestionPart

class MultipartQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'list_of_parts')
    inlines = [
        QuestionPartInline,
    ]
    filter_horizontal = ('tags',)

#admin.site.register(Question)
admin.site.register(SingleQuestion, SingleQuestionAdmin)
admin.site.register(MultipartQuestion, MultipartQuestionAdmin)
#admin.site.register(QuestionPart)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Source)
admin.site.register(Block)
