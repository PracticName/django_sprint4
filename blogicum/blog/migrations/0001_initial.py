# Generated by Django 3.2.16 on 2023-09-28 19:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Тематическая категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('name', models.CharField(max_length=256, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Локация',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category', verbose_name='Категория')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.location', verbose_name='Локация')),
            ],
            options={
                'verbose_name': 'Публикация',
            },
        ),
    ]
