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
    path('delete-product/<str:slug>', views.delete_product, name='delete_product'),
    path('create-cupon/', views.create_cupon, name='create_cupon'),
    path('update-cupon/<cid>/', views.update_cupon, name='update_cupon'),
    path('delete-cupon/<cid>/', views.delete_cupon, name='delete_cupon'),
    path('orders/', views.orders, name='orders'),
    path('ordered-items/<oid>/', views.order_items_details, name='ordered_items'),
    path('update-order-status/<order_id>/', views.update_order_status, name='update_status')
]