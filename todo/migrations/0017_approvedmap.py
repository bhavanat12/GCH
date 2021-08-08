# Generated by Django 3.2.4 on 2021-08-08 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0016_finalmaps_approvalcount'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedMap',
            fields=[
                ('auto_inc', models.AutoField(primary_key=True, serialize=False)),
                ('layerURL', models.TextField(default='https://services3.arcgis.com/nTlnK5Q4GIhY3A7b/arcgis/rest/services/docusign_hackathon/FeatureServer/0')),
                ('mapItem', models.TextField()),
                ('dateSubmitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]