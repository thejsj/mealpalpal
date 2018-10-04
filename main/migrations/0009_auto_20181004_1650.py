# Generated by Django 2.1.1 on 2018-10-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_mealrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealrequest',
            name='city_name',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mealrequest',
            name='meal_name',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mealrequest',
            name='restaurant_id',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mealrequest',
            name='restaurant_name',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
    ]
