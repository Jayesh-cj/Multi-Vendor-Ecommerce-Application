from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.account_login, name='login'),
    path('verify/<str:token>/<str:email>', views.account_activation, name='activate_account'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/<uid>', views.update_profile, name='update')
]