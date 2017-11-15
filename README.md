## 基于Django的在线商店  
  
### **网站主要功能**  
- 可分类产品目录页面  
- 基于`django session`的全局购物车  
- 可接收支付通知的paypal支付网关  
- 定制管理页面，订单管理、订单导出为CSV、生成PDF支票  
- 优惠券系统  
- 添加国际化，支持中文、英文，定制数据库迁移  
- 使用`Redis`构建推荐引擎  
  
### **主要功能实现**  
  
**cart 应用**  
1. 使用 `django sessions`保存购物车，位置`cart.cart`，定义`Cart`类，从`request.session`中取出购物车字段进行编辑，利用生成器建立`__iter__`方法，使`Cart`类为可迭代对象，可依次迭代所有购物车商品。  
2. 创建上下文处理器，将`Cart`类添加进上下文，所有模板都可以使用购物车。  
3. 购物车操作视图。  
  
**orders 应用**  
1. 定制视图扩展管理站点，位置`views.admin_order_detail`，可管理订单信息。  
2. 定制管理站点操作， 到处订单为csv文件，位置`admin.OrderAdmin.export_to_csv()`。  
3. 基于`WeasyPrint`实现订单Pdf导出。  
4. 使用`Celery`实现异步任务，订单完成后发送邮件，位置`task.py`。  
  
**payment 应用**  
1. 基于`django-paypal`集成支付网关到网站。  
2. 使用django-paypal `ipn`信号建立信号接收函数，接收到支付成功信号修改订单为已支付，位置`signals.py`。  
3. 购物车结算视图。  
  
**coupons 应用**  
1. 购物车结算页面添加优惠券表单`CouponApplyForm`，建立`Coupon`模型，结算时显示优惠后价格。  
  
**shop 应用**  
1. 建立`Category model`和`Product model`用来显示商品类别以及列表。  
2. **商品推荐算法**，根据以往订单，通过`Redis`记录订单每件商品与其他商品一起购买的次数，加权算出购物车物品中，以往共同购买次数最多商品的序列，取出部分作为推荐。算法位置`recommender.py`。  
  
**其他**  
1. 部分**代码、模板**翻译，使用`django-rosetta`编辑管理翻译，支持中文、英文，`base.html`模板允许用户手动切换语言。  
2. 使用`django-parler`翻译`models`片段。  
3. 定制无损`translationmodel`迁移，**保留翻译前模型数据**，数据库迁移算法位置`shop.migrations.0003_migrate_translatable_fields.py`。  
  
```
|- django-shop-web
    |- shop\      #app
    |- cart\
    |- coupons\
    |- orders\
    |- payment\
    |- myshop\    #subject
    |- locale\    #translation
    #...
```
