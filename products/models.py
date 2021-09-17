from django.db import models
from django.db.models import base
from django.db.models.deletion import DO_NOTHING, SET_NULL

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.category_name

class Product(models.Model):
    name = models.CharField(max_length=200)
    unitprice = models.IntegerField(blank=False)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=DO_NOTHING, blank=False, null=False)
    size_1 = models.CharField(max_length=10, blank=True)    
    size_2 = models.CharField(max_length=10, blank=True)    
    size_3 = models.CharField(max_length=10, blank=True)    
    color = models.CharField(max_length=50)
    discount = models.IntegerField(default=0)
    photo_main = models.ImageField(upload_to='productimages/%Y/%M/%D/')
    photo_1 = models.ImageField(upload_to='productimages/%Y/%M/%D/', blank=True)
    photo_2 = models.ImageField(upload_to='productimages/%Y/%M/%D/', blank=True)
    photo_3 = models.ImageField(upload_to='productimages/%Y/%M/%D/', blank=True)
    photo_4 = models.ImageField(upload_to='productimages/%Y/%M/%D/', blank=True)
    photo_5 = models.ImageField(upload_to='productimages/%Y/%M/%D/', blank=True)
    photo_6 = models.ImageField(upload_to='productimages/%Y/%M/%D/', blank=True)
    offertill = models.DateTimeField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    is_hot = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


    @property
    def old_price(self):
        price = self.unitprice + (self.discount / 100 * self.unitprice)
        return price

