## 基于Django的在线商店  
  
### **网站主要功能**  
- 可分类产品目录页面  
- 基于`django session`的全局购物车  
- 可接收支付通知的paypal支付网关  
- 定制管理页面，订单管理、订单导出为CSV、生成PDF支票  
- 优惠券系统  
- 添加国际化，支持中文、英文  
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
