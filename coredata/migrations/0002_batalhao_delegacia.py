# Generated by Django 3.1.6 on 2021-02-19 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coredata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batalhao',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('bpm', models.CharField(db_column='bpm', max_length=50)),
                ('municipio', models.CharField(db_column='municipio', max_length=50)),
            ],
            options={
                'db_table': '"basegeo"."policia_areas_dps"',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Delegacia',
            fields=[
                ('id', models.BigIntegerField(db_column='id', primary_key=True, serialize=False)),
                ('nome', models.CharField(db_column='nome', max_length=254)),
                ('municipio', models.CharField(db_column='municipio', max_length=254)),
            ],
            options={
                'db_table': '"basegeo_4326"."policia_delegacias"',
                'managed': False,
            },
        ),
    ]
