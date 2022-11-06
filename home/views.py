from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Category
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin
from order.form import QuantityForm


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = QuantityForm()
        return render(request, 'home/detail.html', {'product': product, 'form': form})


class BucketShowView(IsAdminUserMixin, View):
    def get(self, request):
        buckets = tasks.all_bucket_object_task()
        return render(request, 'home/bucket.html', {'buckets': buckets})


class BucketDeleteView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_bucket_object_task.delay(key)
        messages.success(request, 'object will be delete soon', 'success')
        return redirect('home:show_bucket')


class BucketDownloadView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_bucket_object_task.delay(key)
        messages.success(request, 'object will download soon', 'success')
        return redirect('home:show_bucket')
