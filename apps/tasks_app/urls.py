from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^(?P<id>\d+)$', views.createtask, name='add'),
    url(r'^(?P<id>\d+)/adduser$', views.addusertask, name='adduser'),
    url(r'^(?P<id>\d+)/removeuser$', views.removeusertask, name='removeuser'),
    url(r'^(?P<id>\d+)/delete$', views.deletetask, name='delete'),
    url(r'^(?P<listid>\d+)/(?P<taskid>\d+)/status$', views.changetaskstatus, name='status'),
]
