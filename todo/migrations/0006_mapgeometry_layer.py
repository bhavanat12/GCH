# Generated by Django 3.2.4 on 2021-08-07 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_mapgeometry'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapgeometry',
            name='layer',
            field=models.TextField(default='url'),
            preserve_default=False,
        ),
    ]
