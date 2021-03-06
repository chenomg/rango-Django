#!/usr/bin/env python3
# encoding: utf-8

from django.conf.urls import url, include
from rango import views

app_name = 'rango'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^search/$', views.search, name='search'),
    url(r'^add_profile/$', views.register_profile, name='register_profile'),
    url(r'^like_category/$', views.like_category, name='like_category'),
    url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
    url(r'^goto//?page_id=(?P<page_id>[\d+])/$', views.track_url, name='track_url'),
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^logout/$', views.user_logout, name='logout'),
    # url(r'^restricted/$', views.restricted, name='restricted'),
    # url(r'^register/$', views.register, name='register'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^add_page_from_search/$', views.add_page_from_search, name='add_page_from_search'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        views.add_page,
        name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category,
        name='show_category'),
]
