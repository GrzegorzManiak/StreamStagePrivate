from django.db import models

from store.models import Ticket
from accounts.models import Member

class Order(models.Model):
    purchaser = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL)
    order_id = models.CharField(max_length=32, blank=True)

    purchase_datetime = models.DateTimeField(auto_now_add=True)

    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=10, blank=True)
    billingCountry = models.CharField(max_length=200, blank=True)
    
    # voucher = models.ForeignKey(Voucher, 
    #                             related_name='orders', 
    #                             null=True, 
    #                             blank=True, 
    #                             on_delete=models.SET_NULL)
    # discount = models.IntegerField(default = 0, 
    #                             validators=[MinValueValidator(0), 
    #                             MaxValueValidator(100)])

    def get_items(self):
        return OrderItem.objects.filter(model=self).all()
    
    def get_total(self):
        return sum(OrderItem.objects.filter(model=self).all().values_list('price_paid'))

class OrderItem(models.Model):
    model = models.ForeignKey(Order, null=False, on_delete=models.CASCADE) # orders should not be deleted ever (even if member is deleted)
    ticket = models.ForeignKey(Ticket, null=False, on_delete=models.CASCADE)
    price_paid = models.FloatField()

