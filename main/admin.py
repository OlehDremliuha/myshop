from django.contrib import admin
from .models import Product, Comment, Basket, ProductBasket


admin.site.register(Basket)
admin.site.register(ProductBasket)
admin.site.register(Comment)

# Register your models here.

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'img', 'description', 'price')
    search_fields = ('name',)