# Generated by Django 4.2.3 on 2023-08-07 02:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_reporte_fecha_reporte_hora_alter_solicitud_hora'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100)),
                ('departamento', models.CharField(max_length=100)),
                ('servicio_solicitado', models.TextField()),
                ('servicio_realizado', models.CharField(max_length=100)),
                ('observacion', models.TextField()),
                ('tecnico', models.CharField(max_length=100)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('hora', models.TimeField(default=datetime.time(20, 49, 8, 769982))),
                ('fecha_final', models.DateField(auto_now_add=True)),
                ('hora_final', models.TimeField(default=datetime.time(20, 49, 8, 769982))),
                ('estado', models.CharField(max_length=20)),
                ('prioridad', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='reporte',
            name='hora',
            field=models.TimeField(default=datetime.time(20, 49, 8, 769982)),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='hora',
            field=models.TimeField(default=datetime.time(20, 49, 8, 769982)),
        ),
    ]