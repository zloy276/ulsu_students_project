# Generated by Django 3.2 on 2021-04-17 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nlp', '0006_auto_20210413_1804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='direction',
            name='department',
        ),
        migrations.AddField(
            model_name='direction',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nlp.faculty', verbose_name='Факультет'),
        ),
        migrations.DeleteModel(
            name='Department',
        ),
    ]
