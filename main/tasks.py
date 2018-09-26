from .celery import app
from .models import User, MealRequest
from .util import MealPal
from celery.utils.log import get_logger
logger = get_logger(__name__)

import logging
import os

LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
logging.basicConfig(level=LOGLEVEL)

def handle_error(task, request, status_code):
    logger.exception('Could not book reservation: %r', status_code)
    request.status = 'FAILED'
    request.save()
    task.retry(countdown= 2 ** task.request.retries)

@app.task(bind=True)
def reserve_meal(self, meal_request_id):
    logger.info("Starting %s" % meal_request_id)
    request = MealRequest.objects.get(id=meal_request_id)
    if request:
        instance = request.__dict__
    logger.info("request", instance)
    user = request.user

    request.status = 'ENQUEUED'
    request.save()

    mp = MealPal()

    # Try to login
    status_code = mp.login(user.mealpal_user, user.mealpal_password)
    if status_code != 200:
        return handle_error(self, request, status_code)

    # Once logged in, try to reserve meal
    status_code = mp.reserve_meal_by_schedule_id(instance["meal_id"], instance["time"])
    if status_code != 200:
        return handle_error(self, request, status_code)

    logger.info("Success")
    request.status = 'SUCCESS'
    request.save()
