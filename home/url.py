from django.urls import path, include
from . import views


app_name = 'home'

urlbuckets = [
    path('show/', views.BucketShowView.as_view(), name='show_bucket'),
    path('delete/<key>', views.BucketDeleteView.as_view(), name='delete_bucket'),
    path('download/<key>', views.BucketDownloadView.as_view(), name='download_bucket'),
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>', views.HomeView.as_view(), name='category_filter'),
    path('bucket/', include(urlbuckets)),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
