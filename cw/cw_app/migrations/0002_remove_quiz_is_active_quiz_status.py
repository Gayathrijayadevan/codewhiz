# Generated by Django 5.1.3 on 2024-12-27 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='is_active',
        ),
        migrations.AddField(
            model_name='quiz',
            name='status',
            field=models.TextField(blank=True, null=True),
        ),
    ]
