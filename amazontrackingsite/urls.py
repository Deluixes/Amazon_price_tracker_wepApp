from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products_list/', views.AmazonProductsListView, name='products'),
    path('products_list/<int:product_id>/', views.product_detail_view, name='product-detail'),

]