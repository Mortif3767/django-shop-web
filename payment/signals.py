# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        order.paid = True
        order.save()
        #发送pdf邮件
        subject = 'invoice no.{}'.format(order.id)
        message = 'here is your order invoice.'
        email = EmailMessage(subject,
                             message,
                             settings.PAYPAL_RECEIVER_EMAIL.
                             [order.email])
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out,
                                        stylesheets=stylesheets)
        email.attach('order_{}.pdf'.format(order.id),
                    out.getvalue(),
                    'application/pdf')
        email.send()

valid_ipn_received.connect(payment_notification)