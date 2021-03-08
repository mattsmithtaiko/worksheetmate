from django.db import models
from django.utils.html import format_html_join

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=254)
    def __str__(self):
        return self.name + " (" + str(self.pk) + ")"

class Tag(models.Model):
    name = models.CharField(max_length=254)
    def __str__(self):
        return self.name + " (" + str(self.pk) + ")"
#    def question_list(self):
#        return self.question_set.all()

class Source(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    def __str__(self):
        return self.name + " (" + str(self.pk) + ")"

class Block(models.Model):
    text = models.TextField()
    def __str__(self):
        return self.text + " (" + str(self.pk) + ")"
    def panelbody(self):
        return None
    def is_question(self):
        return hasattr(self, 'question')
    def is_singlequestion(self):
        return hasattr(self, 'question') and hasattr(self.question, 'singlequestion')
    def is_multipartquestion(self):
        return hasattr(self, 'question') and hasattr(self.question, 'multipartquestion')
    def is_worksheetformatblock(self):
        return hasattr(self, 'worksheetformatblock');
    def is_directionsblock(self):
        return hasattr(self, 'worksheetformatblock') and hasattr(self.worksheetformatblock, 'wfbdirections')

class Question(Block):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    date_created = models.DateTimeField(auto_now_add = True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

class SingleQuestion(Question):
    answer = models.TextField()
    def panelbody(self):
        return """ <table class="table-condensed">
            <tr>
            <th>Answer:</th>
            <td>""" + self.answer + """</td>
            </tr>
            <tr>
            <th>Spacing:</th>
            <td>""" + self.spacing + """</td>
            </tr>
            </table>
            """

class MultipartQuestion(Question):
    def list_of_parts(self):
        return '; '.join((qp.text for qp in self.questionpart_set.all())
        )
        # returnString = ""
        # for index, qp in enumerate(self.questionpart_set.all()):
        #     returnString += chr(index + 97) + ") " + qp.text + "<br />"
        # return format_html(returnString)
    def panelbody(self):
        return """ <table class="table-condensed">
            {% for qp in q.multipartquestion.questionpart_set.all|dictsort:"part_order" %}
            <tr>
            <th>{{ forloop.counter|alph }})</th>
            <th>Answer:</th>
            <td>{{ qp.answer }}</td>
            </tr>
            <tr>
            <td></td>
            <th>Spacing:</th>
            <td>{{ qp.spacing }}</td>
            </tr>
            {% endfor %}
            </table>
            """

class QuestionPart(models.Model):
    question = models.ForeignKey(MultipartQuestion, on_delete=models.CASCADE)
    text = models.TextField()
    part_order = models.IntegerField()
    answer = models.TextField()
    num_per_row = models.IntegerField(default=1)
    stretch_factor = models.FloatField(default=1.0)
    def __str__(self):
        return self.text + " (" + str(self.pk) + ")"
