"""mealpalpal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from main import views
from django.urls import include, path

urlpatterns = [
    path('', views.MealRequestListView.as_view(), name='MealRequestListView'),
    path('account', views.UserModifyFormView.as_view(), name='UserModifyFormView'),
    path('request-meal', views.MealRequestFormView.as_view(), name='MealRequestFormView'),
    path('success', views.MealRequestSuccessView.as_view(), name='MealRequestSuccessView'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
