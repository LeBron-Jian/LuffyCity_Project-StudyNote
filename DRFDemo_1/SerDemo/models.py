from django.db import models

# Create your models here.
__all__ = ['Book', 'Publisher', 'Author']

class Book(models.Model):
    title = models.CharField(max_length=32, verbose_name='图书名称')
    CHOICES = ((1, 'Python'), (2, 'Go'), (3, 'Linux'))
    category = models.IntegerField(choices=CHOICES, verbose_name='图书的类别')
    pub_time = models.DateField(verbose_name='图书的出版日期')

    publisher = models.ForeignKey(to='Publisher', on_delete=None)
    author = models.ManyToManyField(to='Author')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '01-图书表'
        db_table = verbose_name_plural


class Publisher(models.Model):
    title = models.CharField(max_length=32, verbose_name='出版社的名称')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '02-出版社表'
        db_table = verbose_name_plural


class Author(models.Model):
    name = models.CharField(max_length=32, verbose_name='作者的姓名')

    def __str(self):
        return self.name

    class Meta:
        verbose_name_plural = '03-作者表'
        db_table =  verbose_name_plural