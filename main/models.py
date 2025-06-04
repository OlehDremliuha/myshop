from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.TextField()

class Product(models.Model):

    categoryId = models.ForeignKey(Category, models.CASCADE)
    name=models.TextField(max_length=50)
    img=models.ImageField(upload_to='', null=True, blank=True)
    description=models.TextField()
    price=models.FloatField()

    def __str__(self):
        return self.name
    


class Comment(models.Model):

    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    comentText = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.comentText
    


class Basket(models.Model):

    userId = models.ForeignKey(User, models.CASCADE)



class ProductBasket(models.Model):

    productId = models.ForeignKey(Product, models.CASCADE)
    basketId = models.ForeignKey(Basket, models.CASCADE)
    productCount = models.IntegerField()

