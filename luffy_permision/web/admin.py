from django.contrib import admin

# Register your models here.

from web.models import Customer, Payment

admin.site.register(Customer)
admin.site.register(Payment)