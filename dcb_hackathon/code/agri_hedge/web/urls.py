from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='Home'),
    #url(r'all_ossec_rules$', views.all_ossec_rules, name='all_ossec_rules'),
]

