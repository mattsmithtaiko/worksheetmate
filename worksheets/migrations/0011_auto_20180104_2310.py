# Generated by Django 2.0 on 2018-01-05 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheets', '0010_auto_20180104_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksheet',
            name='course',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='worksheets.Course'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='question_order',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
