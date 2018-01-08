# Generated by Django 2.0.1 on 2018-01-08 18:55

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20180105_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='id',
            field=models.AutoField(auto_created=True, default='0', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poll',
            name='uid',
            field=models.CharField(default=polls.models.short_urltoken, max_length=40),
        ),
    ]
