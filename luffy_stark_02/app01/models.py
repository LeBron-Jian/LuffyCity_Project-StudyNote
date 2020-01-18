from django.db import models


# Create your models here.
class Depart(models.Model):
    '''
    部门表
    '''
    title = models.CharField(verbose_name="部门名称", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    '''
    用户表
    '''
    name = models.CharField(verbose_name="名称", max_length=32)
    age = models.CharField(verbose_name='年龄', max_length=32)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    depart = models.ForeignKey(verbose_name='部门', to='Depart', on_delete=models.CASCADE)
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.IntegerField(verbose_name="性别", choices=gender_choices, default=1)
    class_choices = (
        (1, '计算1班'),
        (2, '计算2班'),
    )
    classes = models.IntegerField(verbose_name="班级", choices=class_choices, default=1)


    def __str__(self):
        return self.name
