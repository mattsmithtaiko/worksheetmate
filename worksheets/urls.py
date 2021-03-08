from django.urls import path

from . import views

app_name= 'worksheets'
urlpatterns = [
    path('index', views.index, name='index'),
    path('edit/<int:worksheet_pk>/add/<int:block_pk>/<int:index>', views.add_worksheetformatblock, name='add_block'),
#    path('add', views.add, name='add'),
    path('remove/<int:worksheet_pk>', views.remove, name='remove'),
    path('download/<int:worksheet_pk>', views.download, name='download'),
    path('edit/<int:worksheet_pk>/swap/<str:prev_or_next>/<int:block_index>', views.swap_block, name='swap_block'),
    path('edit/<int:worksheet_pk>/remove/<int:block_index>', views.remove_block, name='remove_block'),
    path('edit/<int:worksheet_pk>', views.edit, name='edit'),
]
