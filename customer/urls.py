from django.urls import path
from customer import views

app_name = 'customer'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('prduct/<str:slug>/', views.product_details, name='product')
]