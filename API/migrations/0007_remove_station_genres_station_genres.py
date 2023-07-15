# Generated by Django 4.1.4 on 2023-07-14 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0006_links_remove_country_is_parsed"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="station",
            name="genres",
        ),
        migrations.AddField(
            model_name="station",
            name="genres",
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]