# Generated by Django 4.2.2 on 2023-06-26 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_alter_movie_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='tmbd_id',
            field=models.BigIntegerField(editable=False, verbose_name='TMBD ID'),
        ),
    ]
