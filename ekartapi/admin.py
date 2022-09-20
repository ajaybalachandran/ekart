from django.contrib import admin
from ekartapi.models import Category, Products, Carts, Reviews

# Register your models here.

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Carts)
admin.site.register(Reviews)