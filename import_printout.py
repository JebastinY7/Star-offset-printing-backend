import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "starprinting.settings")
django.setup()

from pricing.models import PriceRule, Category, Size, Variant

with open("printout.json") as f:
    data = json.load(f)

category = Category.objects.get(name="PRINT OUT")

# delete old rows
PriceRule.objects.filter(category=category).delete()

for item in data:
    fields = item["fields"]

    # LOCAL IDs
    local_size_id = fields["size"]
    local_variant_id = fields["variant"]

    # get local size/variant names from JSON model data
    size_name = None
    variant_name = None

    # find size object in json
    for obj in data:
        if obj["model"] == "pricing.size" and obj["pk"] == local_size_id:
            size_name = obj["fields"]["name"]

    # railway size
    size = Size.objects.get(
        category=category,
        name=size_name
    )

    variant = None

    if local_variant_id:

        for obj in data:
            if obj["model"] == "pricing.variant" and obj["pk"] == local_variant_id:
                variant_name = obj["fields"]["name"]

        variant = Variant.objects.get(
            size=size,
            name=variant_name
        )

    PriceRule.objects.create(
        category=category,
        size=size,
        variant=variant,
        min_qty=fields["min_qty"],
        max_qty=fields["max_qty"],
        price=fields["price"],
        shop_discount=fields["shop_discount"],
        cs_discount=fields["cs_discount"],
        notes=fields["notes"]
    )

print("PRINT OUT pricing imported successfully")