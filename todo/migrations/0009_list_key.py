# Generated by Django 2.2.1 on 2019-05-21 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0008_auto_20190520_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='key',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
