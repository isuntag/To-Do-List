from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^loginpage$', views.loginpage, name='loginpage'),
    url(r'^adminregister$', views.admin_registered, name='admin_registered'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^company$', views.company, name='company'),
    url(r'^admins$', views.admin, name='admin'),
    url(r'^users/(?P<id>\d+)$', views.user, name='user'),
]
