from django.contrib import admin

from core.models import Item, ItemOrder, Order

admin.site.register(Item)
admin.site.register(ItemOrder)
admin.site.register(Order)
