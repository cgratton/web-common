# Generated by Django 2.0.3 on 2018-04-16 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_news_item_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='job_listing',
        ),
    ]