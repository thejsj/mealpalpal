from main.tasks import reserve_meal
from django.core.management.base import BaseCommand, CommandError
from datetime import date
from main.models import User, MealRequest
import datetime
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Enqueue meal requests'

    def handle(self, *args, **options):
        print("Obtaining meal requests")
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        try:
            objects = MealRequest.objects.filter(date=tomorrow).values()
        except ObjectDoesNotExist as e:
            self.stdout.write(self.style.SUCCESS('No meal requests found. Done'))
            return
        for o in list(objects):
            reserve_meal.delay(meal_request_id=o["id"])

        #  debug_task.delay()
        self.stdout.write(self.style.SUCCESS('Done'))
