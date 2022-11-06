from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('cart/', views.OrderCartView.as_view(), name='cart'),
    path('create/', views.CreateOrder.as_view(), name='create'),
    path('detail/<int:order_id>/', views.DetailOrder.as_view(), name='detail'),
    path('save/<int:product_id>/', views.SaveQuantity.as_view(), name='save'),
    path('remove/<int:product_id>/', views.RemoveQuantity.as_view(), name='remove'),
    path('apply/<int:order_id>/', views.ApplyCouponView.as_view(), name='apply'),
]
