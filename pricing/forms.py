from django import forms
from .models import Category, Size, Variant, PriceRule, CategoryDiscount, MemberType


# Add Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter category name'
            })
        }


# Add Multiple Sizes under one category
class BulkSizeForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category"
    )

    sizes = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Enter one size per line\nExample:\nA4\nA3\n4x6'
        }),
        help_text="Enter one size per line"
    )

# Bulk Variant
class BulkVariantForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category"
    )

    size = forms.ModelChoiceField(
        queryset=Size.objects.none(),
        empty_label="Select Size"
    )

    variants = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Enter one variant per line\nExample:\nSingle Side\nDouble Side'
        }),
        help_text="Enter one variant per line"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # IMPORTANT:
        # Only load sizes for selected category
        self.fields['size'].queryset = Size.objects.none()

        if 'variant-category' in self.data:
            try:
                category_id = int(self.data.get('variant-category'))

                self.fields['size'].queryset = Size.objects.filter(
                    category_id=category_id
                ).order_by('name')

            except (ValueError, TypeError):
                pass


# Add Price Rule
class PriceRuleForm(forms.ModelForm):
    class Meta:
        model = PriceRule
        fields = [
            'category',
            'size',
            'variant',
            'min_qty',
            'max_qty',
            'price',
            'shop_discount',
            'cs_discount',
        ]

        widgets = {
            'min_qty': forms.NumberInput(attrs={
                'placeholder': 'Minimum quantity'
            }),

            'max_qty': forms.NumberInput(attrs={
                'placeholder': 'Leave empty for Above range'
            }),

            'price': forms.NumberInput(attrs={
                'placeholder': 'Single side price'
            }),

            'shop_discount': forms.NumberInput(attrs={
                'placeholder': 'Shop %'
            }),

            'cs_discount': forms.NumberInput(attrs={
                'placeholder': 'CS %'
            }),

            'notes': forms.TextInput(attrs={
                'placeholder': 'Optional notes'
            }),
        }


    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['size'].queryset = Size.objects.none()
        self.fields['variant'].queryset = Variant.objects.none()

        category_key = None

        if 'price-category' in self.data:
            category_key = 'price-category'
        elif 'category' in self.data:
            category_key = 'category'

        if category_key:
            try:
                category_id = int(self.data.get(category_key))

                self.fields['size'].queryset = Size.objects.filter(
                    category_id=category_id
                ).order_by('name')

            except (ValueError, TypeError):
                pass

            

        # While editing existing rule
        # elif getattr(self.instance, 'category_id', None):
        #     self.fields['size'].queryset = Size.objects.filter(
        #         category=self.instance.category
        #     ).order_by('name')

        elif self.instance.pk:
            self.fields['size'].queryset = Size.objects.filter(
                category=self.instance.category
            ).order_by('name')
            
        size_key = None

        if 'price-size' in self.data:
            size_key = 'price-size'
        elif 'size' in self.data:
            size_key = 'size'

        if size_key:
            try:
                size_id = int(self.data.get(size_key))

                self.fields['variant'].queryset = Variant.objects.filter(
                    size_id=size_id
                ).order_by('display_order', 'name')

            except (ValueError, TypeError):
                pass
        
        elif self.instance and self.instance.pk and self.instance.size_id:
            self.fields['variant'].queryset = Variant.objects.filter(
                size_id=self.instance.size_id
            ).order_by('display_order', 'name')

            if self.instance.variant_id:
                self.initial['variant'] = self.instance.variant_id
            


class CategoryDiscountForm(forms.ModelForm):
    class Meta:
        model = CategoryDiscount

        fields = [
            'category',
            'member_type',
            'discount_percent'
        ]

        widgets = {
            'discount_percent': forms.NumberInput(attrs={
                'placeholder': 'Discount % (Example: 10)'
            }),
        }
