from .celery import app
from .models import User, MealRequest
from .util import MealPal
from celery.utils.log import get_logger
logger = get_logger(__name__)

@app.task(bind=True)
def debug_task(self, meal_request_id):
    logger.info("Starting %s" % meal_request_id)
    request = MealRequest.objects.get(id=meal_request_id)
    user = request.user

    mp = MealPal()

    # Try to login
    status_code = mp.login(user.mealpal_user, user.mealpal_password)
    if status_code != 200:
        logger.exception('Could not login: %r', status_code)
        raise Exception("Could not login")

    # Once logged in, try to reserve meal
    status_code = mp.reserve_meal_by_schedule_id(request.get("meal_id"))
    if status_code != 200:
        logger.exception('Could not book reservation: %r', status_code)
        raise Exception("Could not book")

    logger.info("Success")
