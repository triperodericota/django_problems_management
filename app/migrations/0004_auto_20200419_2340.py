# Generated by Django 3.0.5 on 2020-04-19 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200419_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='resolution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ProblemResolution'),
        ),
    ]
