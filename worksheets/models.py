from django.db import models

from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver

from questions.models import Block, Question

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=254)
    number = models.CharField(max_length=3)
    def __str__(self):
        return self.name

class Worksheet(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254, blank=True, null=True)
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    blocks = models.ManyToManyField(Block, blank=True)
    block_order = models.CharField(max_length=254, blank=True)
    def __str__(self):
        return self.name
    def get_split_block_order(self):
        return self.block_order.split(';')
    def set_block_order(self, block_pks):
        self.block_order = ';'.join(str(bpk) for bpk in block_pks)
    def add_block_to_order(self, block_pk):
        if self.block_order == '': #if this is the first element being added...
            self.block_order = str(block_pk) #don't include the leading semicolon
        else:
            self.block_order += ";" + str(block_pk)
    def add_block_to_order_after(self, block_pk, index):
        order = self.get_split_block_order()
        order.insert(index + 1, block_pk)
        self.set_block_order(order)
    def remove_block_from_order(self, block_index):
        order = self.get_split_block_order()
        order.pop(block_index)
        self.set_block_order(order)
    # def swap_block_orders(self, block_pk1, block_pk2):
    #     order = self.get_split_block_order()
    #     index1 = order.index(str(block_pk1))
    #     index2 = order.index(str(block_pk2))
    #     order[index1], order[index2] = order[index2], order[index1]
    #     self.set_block_order(order)
    def swap_with_previous(self, block_index):
        order = self.get_split_block_order()
        order[block_index-1], order[block_index] = order[block_index], order[block_index-1]
        self.set_block_order(order)
    def swap_with_next(self, block_index):
        order = self.get_split_block_order()
        order[block_index], order[block_index+1] = order[block_index+1], order[block_index]
        self.set_block_order(order)
    def swap_after(self, block_index, new_index):
        order = self.get_split_block_order()
        block_pk = order.pop(block_index)
        order.insert(new_index + 1, block_pk)
        self.set_block_order(order)
    def blocks_in_order(self):
        order = self.get_split_block_order()
        blocks = []
        for bpk in order:
            blocks += [self.blocks.get(pk=int(bpk))]
        return blocks
    def questions_in_order(self):
        if self.block_order == '': #if list completely empty, return None
            return None
        order = self.get_split_block_order()
        questions = []
        for bpk in order:
            block = self.blocks.get(pk=int(bpk))
            if block.is_question():
                questions += [block.question]
        return questions

class WorksheetFormatBlock(Block):
    latex_code = models.TextField(blank = True, null = True)
    def __str__(self):
        return self.text

class WFBDirections(WorksheetFormatBlock):
    directions = models.TextField()
    def __str__(self):
        return self.directions
    #def set_directions(self):
    #    self.latex_code = r'\end{questions}' + "\n\n" + str(directions) + "\n\n" + r'\begin{questions}'

#this updates the block_order list every time either questions.add or questions.remove is called (i.e., you can use the built-in Django functions and still have the list update)
@receiver(m2m_changed, sender=Worksheet.blocks.through)
def blocks_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == 'pre_add':
        for block_pk in pk_set:
            instance.add_block_to_order(block_pk)
    # elif action == 'pre_remove':
    #     for block_pk in pk_set:
    #         instance.remove_block_from_order(block_pk)
    instance.save()

#this updates the direction block's latex_code on save
@receiver(pre_save, sender=WFBDirections)
def directions_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.text ='Directions'
    instance.latex_code = r'\ifthenelse{\boolean{inquestionsenv}}{\end{questions}' + "\n\n" + str(instance.directions) + "\n\n" + r'\begin{questions}}{' + str(instance.directions) + r'}'
