from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='Home'),
    url(r'^fetch_prices$', views.fetch_current_price, name='fetch_prices'),
    url(r'^check_god_mode_inventory$', views.check_god_mode_inventory, name='check_god_mode_inventory'),
    url(r'^loan_inventory$', views.loan_inventory, name='loan_inventory'),
    url(r'^buy_position$', views.buy_position, name='buy_position'),
    url(r'^check_user_inventory$', views.check_user_inventory, name='check_user_inventory'),
]

