import redis
from django.conf import settings
from .models import Product

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommender(object):

    def get_product_key(self, id):
        return 'product:{}:purchased_with'.format(id)

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id),
                             with_id, 1)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            suggestions = r.zrange(self.get_product_key(product_ids[0]),
                                   0, -1, desc=True)[:max_results]
        else:
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)  #https://juejin.im/entry/58e5ed97da2f60005febbdd6
            r.zrem(tmp_key, *product_ids)
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            r.delete(tmp_key)
        suggest_products_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in=suggest_products_ids))
        suggested_products.sort(key=lambda x: suggest_products_ids.index(x.id))
        return suggested_products


    def clear_purchases(self):
        for id in [p.id for p in Product.objects.all()]:
            r.delete(self.get_product_key(id))