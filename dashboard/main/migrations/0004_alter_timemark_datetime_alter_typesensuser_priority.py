# Generated by Django 4.2.11 on 2024-04-18 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_typesensuser_countvals_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemark',
            name='DateTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='typesensuser',
            name='Priority',
            field=models.IntegerField(blank=True),
        ),
    ]
