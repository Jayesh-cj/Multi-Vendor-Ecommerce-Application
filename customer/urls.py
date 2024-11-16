from django.urls import path
from customer import views

app_name = 'customer'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.products, name='products'),
    path('prduct/<str:slug>/', views.product_details, name='product'),
    path('add-to-cart/<pid>/', views.add_to_cart, name="add_to_cart"),
    path('cart/',views.view_cart, name='cart'),
    path('remove-from-cart/<str:slug>/<cid>/', views.remove_from_cart, name='remove_from_cart'),
    path('cupon-verification/', views.cupon_verification, name='cupon-verification'),
    path('filter-products/', views.fillter_products, name='filter'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-address/', views.add_address, name='add_address')
]