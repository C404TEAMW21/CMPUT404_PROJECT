# Generated by Django 3.1.6 on 2021-03-01 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210301_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='followers',
            name='type',
            field=models.CharField(default='followers', editable=False, max_length=9),
        ),
    ]