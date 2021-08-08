# Generated by Django 3.2.4 on 2021-08-07 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0006_mapgeometry_layer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedMaps',
            fields=[
                ('auto_inc', models.AutoField(primary_key=True, serialize=False)),
                ('mapItem', models.TextField()),
                ('layer', models.TextField()),
                ('dateSubmitted', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField()),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
