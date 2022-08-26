from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from .views import SignUpView

urlpatterns = [
    path('', views.index, name='index'),
    path('products_list/', views.AmazonProductsListView, name='products'),
    path('products_list/<int:product_id>/', views.product_detail_view, name='product-detail'),
    path('products_list/delete/<int:id>/', views.followed_product_delete),
    path('login/', LoginView.as_view(authentication_form=CustomLoginForm),name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),

]