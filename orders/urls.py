from django.conf.urls import url
from . import views
from django.utils.translation import gettext_lazy as _


urlpatterns=[
    url(_(r'^create/$'), views.order_create, name='order_create'),
    url(r'^admin/order/(?P<order_id>\d+)/$', views.admin_order_detail, name='admin_order_detail'),
    url(r'^admin/order/(?P<order_id>\d+)/pdf/$', views.admin_order_pdf, name='admin_order_pdf'),
]