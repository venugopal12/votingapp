# Generated by Django 2.0.1 on 2018-01-09 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='_votes',
            new_name='votes',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='total_votes',
        ),
    ]
