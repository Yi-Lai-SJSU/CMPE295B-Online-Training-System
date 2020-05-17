# Generated by Django 3.0.3 on 2020-05-17 03:10

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_auto_20200517_0309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='captions',
        ),
        migrations.AlterField(
            model_name='image',
            name='boxes',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
