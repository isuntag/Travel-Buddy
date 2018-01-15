from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    # catches path of /travels/ and displays the index page just as /travels would
    url(r'^/$', views.index),
    url(r'add$', views.add),
    url(r'add_trip$', views.add_trip),
    url(r'destination/(?P<number>\d+)$', views.view_trip),
    url(r'join_trip/(?P<number>\d+)/(?P<dashboard>\d+)$', views.join_trip),
    url(r'leave_trip/(?P<number>\d+)/(?P<dashboard>\d+)$', views.leave_trip),
    url(r'remove_user/(?P<trip>\d+)/(?P<user>\d+)$', views.remove_user),
    url(r'delete_trip/(?P<number>\d+)$', views.delete_trip),
]
