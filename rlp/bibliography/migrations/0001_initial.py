# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-08 23:52
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion

from rlp.bibliography import choices


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0007_auto_20160114_0641'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('pubmed_id', models.CharField(db_index=True, max_length=100)),
                ('doi', models.CharField(db_index=True, max_length=100)),
                ('source', models.CharField(choices=choices.SOURCE_CHOICES, db_index=True, max_length=25)),
                ('raw_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('project', models.ManyToManyField(through='bibliography.ProjectReference', to='projects.Project')),
            ],
        ),
        migrations.AddField(
            model_name='projectreference',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliography.Reference'),
        ),
    ]