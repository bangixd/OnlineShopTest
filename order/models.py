from django.db import models
from account.models import User
from home.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ('paid', '-updated')

    def __str__(self):
        return f'{self.user} - {self.id}'

    def get_total_price(self):
        total =  sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount = (self.discount / 100) * total
            return total - discount
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.quantity * self.price


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    active = models.BooleanField()
    discount = models.IntegerField(validators=[MaxValueValidator, MinValueValidator])

    def __str__(self):
        return self.code

