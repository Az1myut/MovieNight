# Generated by Django 4.2.2 on 2023-06-26 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Fullname')),
                ('actor_id', models.BigIntegerField(verbose_name='Actor ID')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth Date')),
                ('image', models.ImageField(blank=True, null=True, upload_to='actors/%d%m%Y', verbose_name='Avatar')),
                ('popularity', models.FloatField(blank=True, null=True, verbose_name='Popularity')),
                ('birth_place', models.CharField(blank=True, max_length=255, null=True, verbose_name='Birth Place')),
                ('biography', models.TextField(blank=True, null=True, verbose_name='Biography')),
            ],
            options={
                'verbose_name': 'Actor',
                'verbose_name_plural': 'Actors',
                'ordering': ['-popularity', 'birth_date'],
            },
        ),
    ]
