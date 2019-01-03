
# 独立使用django的model
import sys
import os
#  获取当前文件的路径，以及路径的父级文件夹名
pwd = os.path.dirname(os.path.realpath(__file__))
# 将项目目录加入setting
sys.path.append(pwd + "../")
# manage.py中
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Moocshop.settings')


import django
django.setup()

# 这行代码必须在初始化django之后
from goods.models import Goods, GoodsCategory, GoodsImage

from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail["name"]
    # 将头与尾去掉
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    # 取第一张作为封面图
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""
    # 取出倒数第一个也就是最小的类
    category_name = goods_detail["categorys"][-1]
    # 取出当前子类对应的GoodsCategory对象，filter没有匹配的会返回空数组，不会抛异常。
    # get数据库没有，或者查到两行都是错误
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()
