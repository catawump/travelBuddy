from django.conf.urls import url
from . import views        
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^add$', views.add),
    url(r'^createtrip$', views.createtrip),
    url(r'^trip/(?P<id>\d+)$', views.showtrip),
    url(r'^jointrip/(?P<id>\d+)$', views.jointrip),
    url(r'^logout$', views.logout),
]