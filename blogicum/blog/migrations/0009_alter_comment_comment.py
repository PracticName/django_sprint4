# Generated by Django 3.2.16 on 2023-10-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20231026_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(max_length=256, verbose_name='Комментрарий'),
        ),
    ]
