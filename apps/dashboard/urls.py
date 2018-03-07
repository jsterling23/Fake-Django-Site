from django.conf.urls import url
from . import views


# dashboard urls

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_quote/$', views.add_quote, name='add_quote'),
    url(r'^add_favorite/(?P<quote_id>\d+)/', views.add_favorite, name='add_favorite'),
    url(r'^remove_favorite/(?P<fav_id>\d+)/', views.remove_favorite, name='remove_favorite'),

]
