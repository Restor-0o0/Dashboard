# Generated by Django 4.2.11 on 2024-04-18 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_typesensuser_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typesensuser',
            name='Priority',
            field=models.IntegerField(default=0),
        ),
    ]
