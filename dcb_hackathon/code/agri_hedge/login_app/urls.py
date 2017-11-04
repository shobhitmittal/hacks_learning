from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'login$', views.login_page, name='login_page'),
    url(r'login_verify$', views.login_user, name='login'),
    url(r'logout$', views.logout_user, name='logout'),
]

