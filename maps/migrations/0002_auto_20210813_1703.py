# Generated by Django 3.2.4 on 2021-08-13 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedMap',
            fields=[
                ('auto_inc', models.AutoField(primary_key=True, serialize=False)),
                ('layerURL', models.TextField(default='https://services3.arcgis.com/nTlnK5Q4GIhY3A7b/arcgis/rest/services/docusign_hackathon/FeatureServer/0')),
                ('mapItem', models.TextField()),
                ('dateSubmitted', models.DateTimeField(auto_now_add=True)),
                ('signedBy', models.TextField(default='{}')),
                ('signedCount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CompletedMaps',
            fields=[
                ('auto_inc', models.AutoField(primary_key=True, serialize=False)),
                ('reviewer', models.TextField()),
                ('mapItem', models.TextField()),
                ('layer', models.TextField(default='https://services3.arcgis.com/nTlnK5Q4GIhY3A7b/arcgis/rest/services/docusign_hackathon/FeatureServer/0')),
                ('dateSubmitted', models.DateTimeField(auto_now_add=True)),
                ('comments', models.TextField(default='Enter your comments here')),
                ('status', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FinalMaps',
            fields=[
                ('auto_inc', models.AutoField(primary_key=True, serialize=False)),
                ('mapItem', models.TextField()),
                ('layerURL', models.TextField(default='https://services3.arcgis.com/nTlnK5Q4GIhY3A7b/arcgis/rest/services/docusign_hackathon/FeatureServer/0')),
                ('dateSubmitted', models.DateTimeField(auto_now_add=True)),
                ('approvalCount', models.IntegerField(default=0)),
                ('reviewerReadable', models.TextField(default='False')),
                ('approvedBy', models.TextField(default='{}')),
                ('commentData', models.TextField(default='{}')),
                ('imageData', models.TextField(default='')),
                ('gisUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MapGeometry',
            fields=[
                ('auto_inc', models.AutoField(primary_key=True, serialize=False)),
                ('reviewer', models.TextField()),
                ('mapItem', models.TextField()),
                ('layer', models.TextField(default='https://services3.arcgis.com/nTlnK5Q4GIhY3A7b/arcgis/rest/services/docusign_hackathon/FeatureServer/0')),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('comments', models.TextField(default='Enter your comments here')),
            ],
        ),
        migrations.DeleteModel(
            name='TodoItem',
        ),
    ]