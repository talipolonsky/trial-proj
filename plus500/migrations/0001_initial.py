# Generated by Django 4.0.4 on 2022-04-26 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plus500',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_from', models.CharField(max_length=250)),
                ('ahrefs_rank', models.IntegerField()),
                ('domain_rating', models.IntegerField()),
            ],
        ),
    ]
