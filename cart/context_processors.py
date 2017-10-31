# -*- coding: utf-8 -*-
from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}
'''
用于传给请求上下文（requestcontext），这样改数据就会在请求前后数据可以一直被引用，
而不需要视图函数，一般用于链接到数据库
'''