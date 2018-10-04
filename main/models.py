from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class User(AbstractUser):
    is_staff = models.BooleanField(default=True)

    mealpal_user = models.CharField(max_length=255, default="")
    mealpal_password = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.email

class MealRequest(models.Model):
    city_id = models.CharField(max_length=255)
    # TODO: Change into a model
    city_name = models.CharField(max_length=255) # For View purpose only
    meal_id = models.CharField(max_length=255)
    # TODO: Change into a model
    meal_name = models.CharField(max_length=255) # For View purposes only
    restaurant_id = models.CharField(max_length=255) # For View purposes only
    restaurant_name = models.CharField(max_length=255) # For View purposes only
    time = models.CharField(max_length=255)
    date = models.DateField(default=date.today)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS = (
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('ENQUEUED', 'Enqueued'),
        ('NOT_ENQUEUED', 'Not Enqueued'),
    )
    status = models.CharField(
        max_length=255,
        choices=STATUS,
        default='NOT_ENQUEUED',
    )

    class Meta:
        unique_together = ('user', 'date',)
