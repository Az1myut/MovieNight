# Generated by Django 4.2.2 on 2023-07-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_alter_movie_overview'),
        ('users', '0008_userprofile_favorite_movies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='favorite_movies',
            field=models.ManyToManyField(blank=True, related_name='favorites_people', to='movies.movie', verbose_name='Favorite Movies'),
        ),
    ]