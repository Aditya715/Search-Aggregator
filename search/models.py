from django.db import models

# Create your models here.
class ProductDetail(models.Model):

    product_id = models.CharField(max_length=30, primary_key=True)
    product = models.CharField(max_length=300)
    url = models.URLField()
    image_url = models.URLField()
    price = models.FloatField()
    source = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.product

