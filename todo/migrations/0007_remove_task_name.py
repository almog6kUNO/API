# Generated by Django 2.2.1 on 2019-05-20 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_remove_list_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='name',
        ),
    ]