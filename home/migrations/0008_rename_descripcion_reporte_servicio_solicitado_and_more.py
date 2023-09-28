# Generated by Django 4.2.3 on 2023-08-06 03:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_rename_nombre_solicitante_reporte_usuario_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reporte',
            old_name='descripcion',
            new_name='servicio_solicitado',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='detalle_equipo',
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='hora',
            field=models.TimeField(default=datetime.time(21, 40, 27, 588101)),
        ),
    ]
