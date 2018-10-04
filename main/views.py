from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserModifyForm, MealRequestForm
from .models import User, MealRequest
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .util import MealPal

#  @method_decorator(login_required, name='dispatch')
class UserModifyFormView(FormView):
    template_name = 'user-modify-form.html'
    form_class = UserModifyForm
    success_url = '/success'

    def get_form_kwargs(self):
        form_kwargs = super(UserModifyFormView, self).get_form_kwargs()
        form_kwargs['instance'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)

#  @method_decorator(login_required, name='dispatch')
class MealRequestFormView(FormView):
    template_name = 'meal-request-form.html'
    form_class = MealRequestForm
    success_url = '/success'

    def get_form_kwargs(self):
        form_kwargs = super(MealRequestFormView, self).get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            user = self.request.user
            mp = MealPal()
            mp.login(user.mealpal_user, user.mealpal_password)
            city_name = mp.get_city_by_id(data["city_id"])
            meal = mp.get_meal_by_id(data["city_id"], data["meal_id"])

            # TODO: Add time and city validation
            request = MealRequest(
                city_id=data["city_id"],
                meal_id=data["meal_id"],
                meal_name=meal["meal"]["name"],
                restaurant_id=meal["restaurant"]["id"],
                restaurant_name=meal["restaurant"]["name"],
                date=data["date"],
                user=self.request.user,
                time=data["time"]
                )
            try:
                request.save()
            except IntegrityError as e:
                raise Exception("You already have a meal request for this day")
        return super().form_valid(form)

#  @method_decorator(login_required)
class MealRequestSuccessView(TemplateView):
    template_name = 'success.html'

#  @method_decorator(login_required)
class MealRequestListView(TemplateView):
    template_name = 'request-list.html'

    def meal_requests(self, **kwargs):
        user = self.request.user
        mr = MealRequest.objects.filter(user=user)
        return mr
