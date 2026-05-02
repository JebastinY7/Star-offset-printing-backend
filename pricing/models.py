from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Size(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sizes")
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Variant(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="variants")

    name = models.CharField(max_length=50)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('size', 'name')
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.size.name} - {self.name}"
    

class PriceRule(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True)

    min_qty = models.IntegerField()
    max_qty = models.IntegerField(null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    shop_discount = models.FloatField()

    cs_discount = models.FloatField()

    notes = models.CharField(max_length=255, blank=True, null=True)


    def clean(self):
        if self.max_qty is not None and self.min_qty > self.max_qty:
            raise ValidationError("Min quantity cannot be greater than max quantity")
        
        if self.size.category != self.category:
            raise ValidationError("Size does not belong to selected category")
        
        if self.variant and self.variant.size != self.size:
            raise ValidationError("Variant does not belong to selected size")
    
    def __str__(self):
        return f"{self.category} | {self.size} | {self.variant or 'Default'} ({self.min_qty}-{self.max_qty})"
    
    class Meta:
        unique_together = ('category', 'size', 'variant', 'min_qty', 'max_qty')
        ordering = ['category', 'size', 'min_qty']
    

class MemberType(models.Model):
    name = models.CharField(max_length=50)
    discount_percent = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
class CategoryDiscount(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    member_type = models.ForeignKey(MemberType, on_delete=models.CASCADE)

    discount_percent = models.FloatField()

    class Meta:
        unique_together = ('category', 'member_type')

    def __str__(self):
        return f"{self.category.name} - {self.member_type.name} ({self.discount_percent}%)"

class ShopSettings(models.Model):
    default_discount = models.FloatField()

    def __str__(self):
        return "Shop Settings"