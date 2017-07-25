from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'add$', views.add),
    url(r'add_trip$', views.add_trip),
    url(r'destination/(?P<number>\d+)$', views.view_trip),
    url(r'join_trip/(?P<number>\d+)$', views.join_trip)
]
