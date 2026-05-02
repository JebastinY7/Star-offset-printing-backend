from django.contrib import admin
from .models import Category, Size, Variant, PriceRule, MemberType, ShopSettings, CategoryDiscount


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

    inlines = [VariantInline]

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'size']
    list_filter = ['size']
    search_fields = ['name']


@admin.register(PriceRule)
class PriceRuleAdmin(admin.ModelAdmin):
    list_display = ['category', 'size', 'variant', 'min_qty', 'max_qty', 'price', 'shop_discount', 'cs_discount']
    list_filter = ['category', 'size', 'variant']
    search_fields = ['category__name', 'size__name', 'variant__name']


@admin.register(MemberType)
class MemberTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_percent']


@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    list_display = ['default_discount']

@admin.register(CategoryDiscount)
class CategoryDiscountAdmin(admin.ModelAdmin):
    list_display = ['category', 'member_type', 'discount_percent']
    list_filter = ['category', 'member_type']