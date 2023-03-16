from django.db import models

from store.models import Ticket
from accounts.models import Member

from django.core.validators import MaxValueValidator, MinValueValidator

class Purchase(models.Model):
    purchaser = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL)
    order_id = models.CharField(max_length=32, blank=True)

    purchase_datetime = models.DateTimeField(auto_now_add=True)

    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=10, blank=True)
    billingCountry = models.CharField(max_length=200, blank=True)

    # how much the total was multiplied after summing (pertains to discounts)s
    total_multiplier = models.FloatField(default = 0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    def get_items(self):
        return OrderItem.objects.filter(model=self).all()
    
    def get_total(self):
        return sum(OrderItem.objects.filter(model=self).all().values_list('price_paid')) * self.total_multiplier

class OrderItem(models.Model):
    purchase = models.ForeignKey(Purchase, null=False, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, null=False, on_delete=models.CASCADE)
    price = models.FloatField()

