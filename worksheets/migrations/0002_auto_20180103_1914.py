# Generated by Django 2.0 on 2018-01-03 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksheet',
            name='questions',
            field=models.ManyToManyField(null=True, to='questions.Question'),
        ),
    ]
