# Generated by Django 3.2.4 on 2021-08-08 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0009_finalmaps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedmaps',
            name='reviewer',
            field=models.TextField(),
        ),
    ]
