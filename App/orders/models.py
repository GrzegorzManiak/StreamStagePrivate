from django.db import models
from accounts.models import Member
from django.core.validators import MaxValueValidator, MinValueValidator
from StreamStage.identifiers import new_purchase_id
import uuid

class Purchase(models.Model):
    purchaser = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL)

    purchase_timestamp = models.DateTimeField(auto_now_add=True)

    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=10, blank=True)
    billingCountry = models.CharField(max_length=200, blank=True)

    purchase_id = models.UUIDField(editable=False, null=False, default=uuid.uuid4)
    # how much the total was multiplied after summing (pertains to discounts)s
    total_multiplier = models.FloatField(default = 0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    def get_items(self):
        return PurchaseItem.objects.filter(model=self).all()
    
    def get_total(self):
        return sum(PurchaseItem.objects.filter(model=self).all().values_list('price_paid')) * self.total_multiplier

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, null=False, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=80)
    price = models.DecimalField("Price", decimal_places=2, max_digits=10)

