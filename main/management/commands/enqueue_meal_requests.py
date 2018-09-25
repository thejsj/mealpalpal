from main.tasks import debug_task
from django.core.management.base import BaseCommand, CommandError
from datetime import date
from main.models import User, MealRequest
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Enqueue meal requests'

    def handle(self, *args, **options):
        print("Obtaining meal requests")
        today = date.today()
        try:
            objects = MealRequest.objects.filter(date=today).values()
        except ObjectDoesNotExist as e:
            self.stdout.write(self.style.SUCCESS('No meal requests found. Done'))
            return
        for o in list(objects):
            print('Id', o["id"])
            debug_task.delay(meal_request_id=o["id"])

        #  debug_task.delay()
        self.stdout.write(self.style.SUCCESS('Done'))
