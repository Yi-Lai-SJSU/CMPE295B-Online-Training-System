# Generated by Django 3.0.3 on 2020-03-03 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_model_ispublic'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='label_location',
            field=models.TextField(default='', max_length=360),
        ),
    ]
