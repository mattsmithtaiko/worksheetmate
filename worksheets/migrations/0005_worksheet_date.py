# Generated by Django 2.0 on 2018-01-03 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheets', '0004_auto_20180103_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksheet',
            name='date',
            field=models.DateField(default='2018-01-01'),
            preserve_default=False,
        ),
    ]