from django.urls import path
from . import views

urlpatterns = [
    path('setup/', views.pricing_setup, name='pricing_setup'),
    # path('settings/', views.settings_page, name='settings_page'),
    path('manage/', views.manage_pricing, name='manage_pricing'),
    path('edit-price-rule/<int:rule_id>/', views.edit_price_rule, name='edit_price_rule'),
    path('delete-price-rule/<int:rule_id>/', views.delete_price_rule, name='delete_price_rule'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path("get-sizes/", views.get_sizes, name="get_sizes"),
    path('get-variants/', views.get_variants, name='get_variants'),
    path("digital-price-setup/", views.digital_price_setup, name='digital_price_setup'),
    path("digital-price-table", views.digital_price_table, name='digital_price_table'),
    path("edit-digital-price/<int:id>/", views.edit_digital_price,name="edit_digital_price"),
    path("delete-digital-price/<int:id>/", views.delete_digital_price,name="delete_digital_price"),

]