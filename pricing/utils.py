from django.db.models import Q
from .models import PriceRule

def get_price_rule(category, size, qty):
    return PriceRule.objects.filter(
        category=category,
        size=size,
        min_qty__lte=qty
    ).filter(
        Q(max_qty__gte=qty) | Q(max_qty__isnull=True)
    ).first()