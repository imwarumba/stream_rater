# -*- coding: utf-8 -*-

# from django.conf.urls import url

from stream import views
from django.urls import path


app_name = 'stream'

urlpatterns = [

    path('', views.homepage, name='homepage'),
    path('<slug:category_name_slug>/',
         views.show_category, name='show_category'),
    path('<slug:category_name_slug>/<name>',
         views.show_streamer, name='show_streamer'),
    path('<slug:category_name_slug>/<name>/comment/', views.add_comment, name='add_comment'),
    path('<slug:category_name_slug>/<name>/<id>/discuss/', views.add_sub_comment, name='add_sub_comment'),
    path('stream/register/', views.register, name='register'),
    path('stream/about/', views.about, name='about'),
    path('stream/login/', views.user_login, name='login'),
    path('stream/restricted/', views.restricted, name='restricted'),
    path('stream/logout/', views.user_logout, name='logout'),

]
