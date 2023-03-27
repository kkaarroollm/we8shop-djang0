from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    cat_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.cat_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.cat_name


class Products(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='product_category', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        ordering = ('price',)
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.product.name} - {self.id}"


class SizeOption(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ProductStock(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    size = models.ForeignKey('SizeOption', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name}, {self.size.name}): {self.stock}"

    def set_active_status(self):
        if self.stock > 0:
            self.is_active = True
        else:
            self.is_active = False

    def save(self, *args, **kwargs):
        self.set_active_status()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('product', 'size')
