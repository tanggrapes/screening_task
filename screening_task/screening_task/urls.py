"""screening_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from screening_task.lookup.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"api/lookups", LookUpView, basename='lookups"')
router.register(r"api/values", ValueView, basename='values"')
urlpatterns = [
    url(r"^", include(router.urls)),
    # url(r"^api/values/$", ValueListView.as_view()),
    # url(r"^api/values/(?P<pk>\d+)/$", ValueView.as_view()),
    # url(r"^api/lookups/$", LookUpListView.as_view(), name="lookups-url"),
    # url(r"^api/lookups/(?P<pk>\d+)/$", LookUpView.as_view()),
]
