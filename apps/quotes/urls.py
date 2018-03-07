from django.conf.urls import url
from . import views


# quotes urls

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', views.index, name='index'),
]
