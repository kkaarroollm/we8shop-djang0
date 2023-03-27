from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('store/', views.StoreList.as_view(), name='store'),
    path('store/product/<slug:slug>', views.StoreProductDetail.as_view(), name='product-detail'),
    path('store/<slug:category_slug>', views.StoreByCategory.as_view(), name='category-list')
]