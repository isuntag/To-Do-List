from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^signin$', views.signin),
    url(r'^logout$', views.logout),
    url(r'^company$', views.company),
    url(r'^admins$', views.admin),
    url(r'^createlist$', views.createlist),
    url(r'^lists/(?P<id>\d+)$', views.viewlist)
]
