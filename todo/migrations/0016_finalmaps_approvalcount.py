# Generated by Django 3.2.4 on 2021-08-08 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0015_alter_mapgeometry_reviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalmaps',
            name='approvalCount',
            field=models.IntegerField(default=0),
        ),
    ]
