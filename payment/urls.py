from django.conf.urls import url
from . import views
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    url(_(r'^process/$'), views.payment_process, name='process'),
    url(_(r'^done/$'), views.payment_done, name='done'),
    url(_(r'^canceled/$'), views.payment_canceled, name='canceled'),
]