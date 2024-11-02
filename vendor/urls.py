from django.urls import path
from vendor import views

app_name = 'vendor'

urlpatterns = [
    path('home/', views.homepage, name='homepage'),
    path('products/', views.view_products, name='products')
]