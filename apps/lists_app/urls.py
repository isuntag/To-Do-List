from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^(?P<id>\d+)$', views.createviewlist, name='add'),
    url(r'^(?P<id>\d+)/delete$', views.deletelist, name='delete'),
    url(r'^(?P<id>\d+)/adduser$', views.adduserlist, name='adduser'),
    url(r'^(?P<id>\d+)/removeuser$', views.removeuserlist, name='removeuser'),
    url(r'^(?P<id>\d+)/list_users', views.list_users, name='list_users'),
]
