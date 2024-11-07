from django.urls import path
from vendor import views

app_name = 'vendor'

urlpatterns = [
    path('home/', views.homepage, name='homepage'),
    path('products/', views.view_products, name='products'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-color/', views.add_color_variant, name='add_color'),
    path('add-size/', views.add_size_variant, name='add_size'),
    path('delete-product/<str:slug>', views.delete_product, name='delete_product')
]