from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'^main$', views.index),  # login page
    url(r'login$', views.log_in),  # login verifies and redirects to succes
    url(r'users$', views.register),  # register verifies and redirects to success
    url(r'success$', views.success),  # success redirects to landing page (here, quotes)
    url(r'dashboard$', views.dashboard),  # renders landing page
    url(r'wish_items/(?P<id>\d+)$', views.wish_items), # user details
    url(r'post_item$', views.post_item),  # posts to site
    url(r'join/(?P<id>\d+)$', views.join), 
    url(r'remove$', views.remove),
    url(r'signout$', logout, {'next_page': '/main'}, name='logout')  # logout user
]