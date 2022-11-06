from django.shortcuts import render, get_object_or_404, redirect
from home.models import Product
from django.views import View
from .cart import Cart
from .form import QuantityForm, CouponForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Order, OrderItem, Coupon
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import PermissionDenied


class OrderCartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'order/cart.html', {'cart': cart})


class SaveQuantity(PermissionRequiredMixin, View):
    permission_required = 'order.add_order'

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = QuantityForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('order:cart')


class RemoveQuantity(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('order:cart')


class DetailOrder(LoginRequiredMixin, View):
    def get(self, request, order_id):
        form = CouponForm()
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'order/order.html', {'order': order, 'form': form})


class CreateOrder(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()
        return redirect('order:detail', order.id)


class ApplyCouponView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        now = datetime.now()
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, from_date__lte=now, to_date__gt=now , active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'coupon not found')
                return redirect('order:detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            return redirect('order:detail', order_id)




