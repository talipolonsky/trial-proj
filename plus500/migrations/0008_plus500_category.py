# Generated by Django 3.2.13 on 2022-05-21 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plus500', '0007_settings_table_links_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='plus500',
            name='category',
            field=models.CharField(blank=True, choices=[('news', 'news'), ('finance', 'finance'), ('crypto', 'crypto'), ('forex', 'forex'), ('commodities', 'commodities'), ('leisure', 'leisure')], max_length=50),
        ),
    ]
