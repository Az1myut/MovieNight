# Generated by Django 4.2.2 on 2023-07-14 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_movie_likes_count'),
        ('users', '0011_alter_userprofile_movie_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='liked_movies',
            field=models.ManyToManyField(blank=True, related_name='liked_by_users', to='movies.movie', verbose_name='Liked Movies'),
        ),
    ]
