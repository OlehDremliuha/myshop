from django.db import models

class Product(models.Model):

    name=models.TextField(max_length=50)
    img=models.ImageField(upload_to='', null=True, blank=True)
    description=models.TextField()
    price=models.FloatField()

    def __str__(self):
        return self.name