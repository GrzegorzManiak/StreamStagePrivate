from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

class Purchase(models.Model):
    purchaser = models.ForeignKey('accounts.Member', null=True, blank=True, on_delete=models.SET_NULL)

    purchase_timestamp = models.DateTimeField(auto_now_add=True)

    stripe_id = models.CharField(max_length=250, blank=True)
    payment_id = models.CharField(max_length=250, blank=True)

    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=10, blank=True)
    billingCountry = models.CharField(max_length=200, blank=True)

    purchase_id = models.UUIDField(editable=False, null=False, default=uuid.uuid4)
    # how much the total was multiplied after summing (pertains to discounts)s
    total_multiplier = models.FloatField(default = 0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    def get_items(self):
        return PurchaseItem.objects.filter(purchase=self).all()
    
    def get_serialized_items(self):
        return [item.serialize() for item in self.get_items()]
    
    def get_total(self):
        items = PurchaseItem.objects.filter(purchase=self).all().values_list('price')
        total = 0
        for item in items:
            total += float(item[0])

        return total * self.total_multiplier
    
    def serialize(self):
        return {
            "purchase_id": self.purchase_id,
            "purchase_timestamp": self.purchase_timestamp,
            "billingName": self.billingName,
            "billingAddress1": self.billingAddress1,
            "billingCity": self.billingCity,
            "billingPostcode": self.billingPostcode,
            "billingCountry": self.billingCountry,
            "total": self.get_total(),
            "stripe_id": self.stripe_id,
            "payment_id": self.payment_id,
            "items": [item.serialize() for item in self.get_items()]
        }

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, null=False, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=80)
    price = models.DecimalField("Price", decimal_places=2, max_digits=10)
    other_data = models.CharField(max_length=2500, blank=True)

    def serialize(self):
        return {
            "item_name": self.item_name,
            "price": self.price,
            "other_data": self.other_data,
        }