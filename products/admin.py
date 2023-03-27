from django.contrib import admin
from .models import Category, Products, ProductStock, SizeOption, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('cat_name',)}


class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 1


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(ProductImage)
class ProductImage(admin.ModelAdmin):
    pass


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('price', 'category')
    search_fields = ('name', 'price')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'description', 'price', 'category', 'slug')
    inlines = [ProductStockInline, ProductImageInline]


@admin.register(SizeOption)
class SizeOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'stock', 'is_active')
    list_filter = ('is_active', 'size')
