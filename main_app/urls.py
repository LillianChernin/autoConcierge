from django.conf.urls import url
from .views import main, car_owner, shop_owner, service_driver

urlpatterns = [
    url(r'^$', main.index),
    url(r'^signup/$', main.signup),
    url(r'^signup/carowner/$', car_owner.SignUpView.as_view(), name='car_owner_signup'),
    url(r'^signup/shopowner/$', shop_owner.SignUpView.as_view(), name='shop_owner_signup'),
    url(r'^signup/servicedriver/$', service_driver.SignUpView.as_view(), name='service_driver_signup'),
    url(r'^([0-9]+)/car-owner-profile/$', main.profile_car_owner, name='car_owner_profile'),
    url(r'^([0-9]+)/shop-owner-profile/$', main.profile_shop_owner, name='shop_owner_profile'),
    url(r'^([0-9]+)/service-driver-profile/$', main.profile_service_driver, name='service_driver_profile'),
]