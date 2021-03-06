# Generated by Django 2.1.2 on 2018-10-11 17:23

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('details', django.contrib.postgres.fields.jsonb.JSONField()),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
            ],
        ),
    ]
