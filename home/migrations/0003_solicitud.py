# Generated by Django 4.2.3 on 2023-08-01 01:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_diagnostico'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento', models.CharField(max_length=100)),
                ('detalle_equipo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('solcitudes', models.CharField(max_length=100)),
                ('estado', models.CharField(choices=[('En espera', 'En espera'), ('pendiente', 'Pendiente'), ('Terminado', 'Terminado'), ('Cancelado', 'Cancelado'), ('en proceso', 'En proceso'), ('aceptado', 'Aceptado')], default='En espera', max_length=20)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('hora', models.TimeField(default=datetime.time(19, 36, 20, 628939))),
                ('prioridad', models.CharField(default='bajo', max_length=100)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]