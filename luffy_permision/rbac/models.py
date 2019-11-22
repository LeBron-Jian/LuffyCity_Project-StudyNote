from django.db import models


# Create your models here.

class Menu(models.Model):
    '''
    菜单
    '''
    title = models.CharField(verbose_name="菜单名称", max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32)

    def __str__(self):
        return self.title


class Permission(models.Model):
    '''
    权限表
    '''
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的url', max_length=128)

    # 按理来说，，不该为空，但是我们数据库的表已经有了，所以，。。。
    name = models.CharField(verbose_name='URL别名', max_length=32, unique=True)

    # is_menu = models.BooleanField(verbose_name='是否可以做菜单', default=False)
    # null 表示数据为空，black表示django可以为空
    # icon = models.CharField(verbose_name="图标",max_length=32, null=True, blank=True)

    menu = models.ForeignKey(verbose_name="所属菜单", to='Menu', null=True, blank=True,
                             help_text='null表示不是菜单;非null表示是二级菜单', on_delete=models.CASCADE)

    pid = models.ForeignKey(verbose_name='关联的权限', to='Permission',
                            null=True, blank=True, on_delete=models.CASCADE,
                            related_name='parents',
                            help_text='对于非菜单权限需要选择一个可以称为菜单的权限，用户做默认展开和选择菜单')

    def __str__(self):
        return self.title


class Role(models.Model):
    '''
    角色
    '''
    title = models.CharField(verbose_name='角色名称', max_length=32)

    permissions = models.ManyToManyField(verbose_name="拥有的所有权限",
                                         to='Permission',
                                         blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    '''
    用户表
    '''
    name = models.CharField(verbose_name="用户名", max_length=332)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name="邮箱", max_length=128)

    roles = models.ManyToManyField(verbose_name="拥有的所有角色",
                                   to='Role',
                                   blank=True)

    def __str__(self):
        return self.name


"""
current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()

# 获取当前用户所拥有的权限
permission_list = current_user.roles.filter(permissions__isnull=False).values(permissions__id,permissions__url).distinct()

# 问题一：
    1. 一个用户是否可以拥有多个角色？是
    2. 一个角色是否可以用拥有多个权限？是

    CEO：
        /index/
        /order/
    总监：
        /index/
        /customer/

    销售：
        /user/
        /add_user/
    金牌讲师

# 问题二：
    权限表：
        /index/
        ....

    角色表：
        CEO：
        总监：
        销售：
        金牌讲师

    角色和权限关系：
         CEO：     /index/
         总监：     /order/

    用户和角色关系表：
        1 1 
        1 1 
        1 1 

    用户表：
        wupeiqi



总监 /index/
总监 /customer/
销售 /user/
销售 /add_user/
金牌讲师 null

"""
