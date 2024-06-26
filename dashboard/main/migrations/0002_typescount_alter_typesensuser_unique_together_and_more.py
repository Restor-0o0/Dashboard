# Generated by Django 4.2.11 on 2024-04-17 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypesCount',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Nume', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='typesensuser',
            unique_together={('User', 'Type', 'DrawingType')},
        ),
        migrations.AddField(
            model_name='typesensuser',
            name='CountVals',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='typesensuser',
            name='TypeCount',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.typescount'),
        ),
    ]
