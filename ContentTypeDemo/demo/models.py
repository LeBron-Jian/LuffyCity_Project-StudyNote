from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


# Create your models here.
class Food(models.Model):
    '''
    id    title
    1      面包
    2      牛奶
    '''
    title = models.CharField(max_length=32)
    # 不会生成字段，只用于反向查询
    coupons = GenericRelation(to='Coupon')


class Fruit(models.Model):
    '''
    id    title
    1      苹果
    2      香蕉
    '''
    title = models.CharField(max_length=32)


# 如果有40张表
# class  Coupon(models.Model):
#     '''
#     id    title
#     1      面包
#     2      牛奶
#     '''
#     title = models.CharField(max_length=32)
#     food = models.ForeignKey(to='Food', on_delete=None)
#     fruit = models.ForeignKey(to='Fruit', on_delete=None)

class Coupon(models.Model):
    """
    优惠券表
    id  name    appliance_id    food_id     fruit_id
    1   通用优惠券   null            null        null
    2   冰箱折扣券   1               null        null
    3   电视折扣券   2               null        null
    4   苹果满减卷   null            null        1
    我每增加一张表就要多增加一个字段
    """
    title = models.CharField(max_length=32)
    # appliance = models.ForeignKey(to="Appliance", null=True, blank=True)
    # food = models.ForeignKey(to="Food", null=True, blank=True)
    # fruit = models.ForeignKey(to="Fruit", null=True, blank=True)
    # 第一步
    content_type = models.ForeignKey(to=ContentType, on_delete=None)
    # 第二步
    object_id = models.PositiveIntegerField()
    # 第三步
    content_object = GenericForeignKey('content_type', 'object_id')

# class Table(models.Model):
#     '''
#     # 注意这里的app_name  是说一个大项目中有多个APP
#     id   app_name    table_name
#     1     demo        food
#     2     demo        fruit
#     '''
#     app_name = models.CharField(max_length=32)
#     table_name = models.CharField(max_length=32)
