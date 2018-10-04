from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, MealRequest
from .util import MealPal
import datetime
from django.forms.models import model_to_dict
from django.forms import ModelForm, Form

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')

class UserModifyForm(ModelForm):
    class Meta:
        model = User
        fields = ['mealpal_user', 'mealpal_password']

def get_city_obj(x):
    return (x["objectId"], x["name"],)

def get_meal_obj(x):
    print('get_meal_obj')
    print(x)
    import json
    print(json.dumps(x))
    print(x["meal"], x["restaurant"])
    name = x["meal"]["name"] + " " + x["restaurant"]["name"]
    return (x["id"], name)

def tomorrow():
    today = datetime.date.today()
    return today + datetime.timedelta(days=1)

def get_times():
    return [
        ("11:30am-11:45am", "11:30", ),
        ("11:45am-12:00pm", "11:45", ),
        ("12:00pm-12:15pm", "12:00", ),
        ("12:15pm-12:30pm", "12:15", ),
        ("12:30pm-12:45pm", "12:30", ),
        ("12:45pm-1:00pm", "12:45", )
        ]

class MealRequestForm(forms.Form):
    city_id= forms.ChoiceField(choices=[])
    meal_id = forms.ChoiceField(choices=[])
    date = forms.DateField(initial=tomorrow)
    # TODO: Fix times to query from meal
    time = forms.ChoiceField(initial="12:15",choices=get_times())

    def __init__(self, *args, **kwargs):
        user = model_to_dict(kwargs["user"])
        del kwargs["user"]
        super(MealRequestForm, self).__init__(*args, **kwargs)

        # TODO: Cache logins requests depending on city
        mp = MealPal()
        status_code = mp.login(user["mealpal_user"], user["mealpal_password"])
        if status_code != 200:
            raise Exception("Could not login to MealPal with your credentials")

        cities = list(map(get_city_obj, mp.get_cities()))
        sf_object_id = list(filter(lambda x : x[1] == "San Francisco", cities))[0]
        meal_response = mp.get_schedules(None, sf_object_id[0])
        meals = list(map(get_meal_obj, meal_response))

        self.fields['city_id'] = forms.ChoiceField(
            choices=cities,
            initial=sf_object_id,
            widget=forms.Select(attrs={'readonly':'readonly', 'class': 'selectpicker', 'data-live-search': 'true'}),
            required=True
        )
        self.fields['meal_id'] = forms.ChoiceField(
            choices=meals,
            widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            required=True
        )
