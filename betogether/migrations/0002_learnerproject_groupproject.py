# Generated by Django 3.2.5 on 2022-05-30 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('betogether', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='learnerproject',
            name='groupProject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='betogether.groupproject'),
        ),
    ]
