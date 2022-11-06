from django import forms


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)


class CouponForm(forms.Form):
    code = forms.CharField()