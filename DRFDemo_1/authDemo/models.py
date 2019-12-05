from django.db import models

# Create your models here.
__all__ = ['User']


class User(models.Model):
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=16)
    token = models.UUIDField()
    type = models.IntegerField(choices=((1, 'VIP'),
                                        (2, "SVIP"),
                                        (3, 'Oridinary')),
                               default=3)
