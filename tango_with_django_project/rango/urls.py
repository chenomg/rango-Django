#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
