from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Size, Variant, PriceRule, MemberType, CategoryDiscount
from .forms import CategoryForm, BulkSizeForm,BulkVariantForm, PriceRuleForm, CategoryDiscountForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.urls import reverse


@login_required
def settings_page(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    
    categories = Category.objects.all()
    sizes = Size.objects.all()
    price_rules = PriceRule.objects.all()
    members = MemberType.objects.all()

    return render(request, "pricing/settings.html", {
        "categories": categories,
        "sizes": sizes,
        "price_rules": price_rules,
        "members": members
    })


@login_required
def pricing_setup(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)

    # Empty forms for page load
    category_form = CategoryForm(prefix='cat')
    size_form = BulkSizeForm(prefix='size')
    variant_form = BulkVariantForm(prefix='variant')
    price_form = PriceRuleForm(prefix='price')
    discount_form = CategoryDiscountForm(prefix = 'discount')

    if request.method == "POST":

        if 'add_category' in request.POST:
            category_form = CategoryForm(request.POST, prefix='cat')

            if category_form.is_valid():
                category_form.save()
                return redirect('pricing_setup')

        elif 'add_sizes' in request.POST:
            size_form = BulkSizeForm(request.POST, prefix='size')

            if size_form.is_valid():
                category = size_form.cleaned_data['category']
                sizes_text = size_form.cleaned_data['sizes']

                size_list = [
                    s.strip() for s in sizes_text.splitlines() if s.strip()
                ]

                for size_name in size_list:
                        # Prevent duplicate sizes
                        Size.objects.create(
                            category=category,
                            name=size_name
                        )

                return redirect('pricing_setup')
            
        elif 'add_variants' in request.POST:
            variant_form = BulkVariantForm(request.POST, prefix='variant')

            if variant_form.is_valid():
                size = variant_form.cleaned_data['size']

                variants_text = variant_form.cleaned_data['variants']

                variant_list = [v.strip() for v in variants_text.splitlines() if v.strip()
                ]

                for index, variant_name in enumerate(variant_list):
                    Variant.objects.get_or_create(
                        size=size,
                        name=variant_name,
                        defaults={
                            "display_order": index
                        }
                    )
                
                return redirect('pricing_setup')

        
        elif 'add_price_rule' in request.POST:
            category_id = request.POST.get("price-category")
            size_id = request.POST.get("price-size")

            min_qty = request.POST.get("price-min_qty") or 1
            max_qty = request.POST.get("price-max_qty") or None

            shop_discount = request.POST.get("price-shop_discount") or 0
            cs_discount = request.POST.get("price-cs_discount") or 0
            notes = request.POST.get("price-notes") or ""

            # MULTIPLE ROWS
            variants = request.POST.getlist("variant[]")
            prices = request.POST.getlist("price[]")

            # SAVE EACH VARIANT
            for variant_id, price in zip(variants, prices):

                if not variant_id or not price:
                    continue

                try:
                    PriceRule.objects.create(
                    category_id=category_id,
                    size_id=size_id,
                    variant_id=variant_id,
                    min_qty=min_qty,
                    max_qty=max_qty,
                    price=price,
                    shop_discount=shop_discount,
                    cs_discount=cs_discount,
                    notes=notes
                    )
                except IntegrityError:
                    messages.error(
                        request,
                        f"{variant_id} already exists for this size and quantity range."
                    )

            return redirect("pricing_setup")
            

            
        elif 'add_category_discount' in request.POST:
            discount_form = CategoryDiscountForm(request.POST, prefix='discount')

            if discount_form.is_valid():
                discount_form.save()

                return redirect('pricing_setup')

    # Fetch all categories for display tables
    #categories = Category.objects.all()

    return render(request, 'pricing/setup.html', {
        'category_form': category_form,
        'size_form': size_form,
        'variant_form': variant_form,
        'price_form': price_form,
        'discount_form': discount_form,
        # 'categories': categories,
    })

@login_required
def get_sizes(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)

    category_id = request.GET.get("category_id")

    sizes = Size.objects.filter(
        category_id=category_id
    ).order_by("name").values(
        "id",
        "name"
    )

    return JsonResponse({
        "sizes": list(sizes)
    })


# 🔥 GET VARIANTS BY SIZE
@login_required
def get_variants(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)

    size_id = request.GET.get("size_id")

    variants = Variant.objects.filter(
        size_id=size_id
    ).order_by("display_order", "name").values("id", "name")

    return JsonResponse({
        "variants": list(variants)
    })

# Edit Price Rule
@login_required
def edit_price_rule(request, rule_id):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    
    rule = get_object_or_404(PriceRule, id=rule_id)

    if request.method == "POST":

        form = PriceRuleForm(request.POST, instance=rule)

        # POST category
        category_id = request.POST.get("category")

        if category_id:
            form.fields['size'].queryset = Size.objects.filter(
                category_id=category_id
            ).order_by("name")

        if form.is_valid():
            form.save()
            page = request.POST.get("page", "")
            category = request.POST.get("category", "")
            search = request.POST.get("search", "")

            url = reverse("manage_pricing")

            return redirect(
                f"{url}?page={page}&category={category}&search={search}"
            )

    else:
        # GET page open
        form = PriceRuleForm(instance=rule)

        # 🔥 USE rule.category_id DIRECTLY
        form.fields['size'].queryset = Size.objects.filter(
            category_id=rule.category_id
        ).order_by("name")

        form.initial['size'] = rule.size_id

    return render(request, "pricing/edit_price_rule.html", {
        "form": form,
        "rule": rule
    })

@login_required
def manage_pricing(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)

    search = request.GET.get("search", "")
    category_filter = request.GET.get("category", "")

    categories = Category.objects.all().order_by("name")

    rules = PriceRule.objects.select_related(
        "category", "size", "variant"
    ).order_by("category__name", "size__name", "min_qty")

    if search:
        rules = rules.filter(category__name__icontains=search)

    if category_filter:
        try:
            rules = rules.filter(category__id=int(category_filter))
        except ValueError:
            pass

    paginator = Paginator(rules, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "pricing/manage_pricing.html", {
        "page_obj": page_obj,
        "categories": categories,
        "search": search,
        "selected_category": category_filter,
    })


@login_required
def delete_price_rule(request, rule_id):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    
    rule = get_object_or_404(PriceRule, id=rule_id)

    rule.delete()

    return redirect("manage_pricing")

# Delete Full Category
@login_required
def delete_category(request, category_id):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)

    category = get_object_or_404(Category, id=category_id)

    # Delete all related price rules first
    PriceRule.objects.filter(category=category).delete()

    # Delete all related sizes
    Size.objects.filter(category=category).delete()

    # Delete category itself
    category.delete()

    return redirect("manage_pricing")