from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('verify/', views.UserRegisterVerifyView.as_view(), name='user_verify'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
]
