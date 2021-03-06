# Generated by Django 2.1.1 on 2018-09-25 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20180925_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealrequest',
            name='city_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='mealrequest',
            name='meal_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='mealrequest',
            name='time',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='mealrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='mealrequest',
            unique_together={('user', 'date')},
        ),
    ]
