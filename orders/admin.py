# -*- coding: utf-8 -*-
import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import Order, OrderItem
from django.core.urlresolvers import reverse


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y') #将时间转换成字符串
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    return '<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id]))
order_detail.allow_tags = True #允许html输出


def order_pdf(obj):
    return '<a href="{}">Export pdf</a>'.format(
        reverse('orders:admin_order_pdf', args=[obj.id]))
order_pdf.allow_tags = True
order_pdf.short_description = 'Electric bill'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]  #内联元素允许在同一编辑页引用模型
    actions = [export_to_csv]

admin.site.register(Order, OrderAdmin)
