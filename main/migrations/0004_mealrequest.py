# Generated by Django 2.1.1 on 2018-09-22 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180921_2358'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(default='', max_length=255)),
                ('restaurant_name', models.CharField(default='', max_length=255)),
                ('timing', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
