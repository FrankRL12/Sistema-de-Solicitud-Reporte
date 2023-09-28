# Generated by Django 4.2.3 on 2023-07-21 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostico',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('marca', models.CharField(max_length=50)),
                ('n_serie', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('ubicacion', models.CharField(max_length=30)),
                ('diagnostico', models.TextField()),
                ('solucion', models.TextField()),
                ('estado', models.CharField(choices=[('activo', 'activo'), ('en reparacion', 'en reparacion'), ('de vaja', 'de vaja')], max_length=20)),
            ],
            options={
                'verbose_name': 'diagnostico',
                'verbose_name_plural': 'diagnosticos',
            },
        ),
    ]