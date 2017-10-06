from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^adminregister$', views.admin_registered),
    url(r'^signin$', views.signin),
    url(r'^logout$', views.logout),
    url(r'^company$', views.company),
    url(r'^admins$', views.admin),
    url(r'^createlist/(?P<id>\d+)$', views.createlist),
    url(r'^lists/delete/(?P<id>\d+)$', views.deletelist),
    url(r'^lists/(?P<id>\d+)$', views.viewlist),
    url(r'^list/adduser/(?P<id>\d+)$', views.adduserlist),
    url(r'^list/removeuser/(?P<id>\d+)$', views.removeuserlist),
    url(r'^createtask/(?P<listid>\d+)$', views.createtask),
    url(r'^tasks/adduser/(?P<id>\d+)$', views.addusertask),
    url(r'^tasks/removeuser/(?P<id>\d+)$', views.removeusertask),
    url(r'^tasks/delete/(?P<id>\d+)$', views.deletetask),
    url(r'^tasks/status/(?P<taskid>\d+)/(?P<listid>\d+)$', views.changetaskstatus),
    url(r'^users/(?P<id>\d+)$', views.userpage),
    url(r'^updateuser/(?P<id>\d+)$', views.updateuser)
]
