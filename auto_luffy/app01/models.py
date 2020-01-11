from django.db import models

# Create your models here.
from rbac.models import UserInfo as RbacUserInfo


class Department(models.Model):
    '''
    部门表
    '''
    title = models.CharField(verbose_name='部门', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(RbacUserInfo):
    phone = models.CharField(verbose_name='联系方式', max_length=32)
    level_choices = (
        (1, 'T1'),
        (2, 'T2'),
        (3, 'T3'),
    )
    level = models.IntegerField(verbose_name='级别', choices=level_choices)
    # on_delete=models.CASCADE表示级联删除，当删除主表的数据时，从表的数据也随着一起删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", on_delete=models.CASCADE)


class Host(models.Model):
    hostname = models.CharField(verbose_name='主机名称', max_length=32)
    ip = models.GenericIPAddressField(verbose_name='IP', protocol='both')
    depart = models.ForeignKey(verbose_name='归属部门', to='Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname
