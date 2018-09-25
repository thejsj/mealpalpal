from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserModifyForm, MealRequestForm
from .models import User, MealRequest
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

@method_decorator(login_required, name='dispatch')
class UserModifyFormView(FormView):
    template_name = 'form.html'
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

@method_decorator(login_required, name='dispatch')
class MealRequestFormView(FormView):
    template_name = 'form.html'
    form_class = MealRequestForm
    success_url = '/success'

    def get_form_kwargs(self):
        form_kwargs = super(MealRequestFormView, self).get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            # TODO: Add time and city validation
            request = MealRequest(city_id=data["city_id"], meal_id=data["meal_id"], date=data["date"], user=self.request.user, time=data["time"])
            try:
                request.save()
            except IntegrityError as e:
                raise Exception("You already have a meal request for this day")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class MealRequestSuccessView(TemplateView):
    template_name = 'success.html'
