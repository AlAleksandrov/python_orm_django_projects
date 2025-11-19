import os


import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from orm_skeleton.helpers import populate_model_with_data
from main_app.models import Profile, Product, Order
from django.db.models import Q, Count, F, When, Value, Case
from typing import Optional
from main_app.querysets import ProfileQuerySet

# Create queries within functions

def populate_db() -> None:
    populate_model_with_data(Profile)
    populate_model_with_data(Product)
    populate_model_with_data(Order)


def get_profiles(search_string: Optional[str]=None) -> str:
    if not search_string:
        return ''

    profiles_match = Profile.objects.filter(
        Q(full_name__icontains=search_string)
            |
        Q(email__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    return '\n'.join(
        f'Profile: {pm.full_name}, '
        f'email: {pm.email}, '
        f'phone number: {pm.phone_number}, '
        f'orders: {pm.order_set.count()}'
        for pm in profiles_match
    )

def get_loyal_profiles() -> str:
    loyal_profiles = Profile.objects.get_regular_customers()

    if not loyal_profiles:
        return ''

    return '\n'.join(
        f'Profile: {lp.full_name}, '
        f'orders: {lp.count_orders}'
        for lp in loyal_profiles
    )

def get_last_sold_products() -> str:
    last_order = Order.objects.last()

    if not last_order:
        return ''

    return f"Last sold products: {', '.join(p.name for p in last_order.products.all())}"


def get_top_products() -> str:
    top_products = Product.objects.annotate(
        orders_count=Count('order')
    ).filter(
        orders_count__gt=0
    ).order_by(
        '-orders_count',
        'name'
    )[:5]

    if not top_products:
        return ''

    return f'Top products:\n' + '\n'.join(
        f'{p.name}, sold {p.orders_count} times'
        for p in top_products
    )

def apply_discounts() -> str:
    updated_orders = Order.objects.annotate(
        products_count=Count('products')
    ).filter(
        products_count__gt=2,
        is_completed=False
    ).update(
        total_price=F('total_price') * 0.90
    )

    if not updated_orders:
        return ''

    return f'Discount applied to {updated_orders} orders'

def complete_order() -> str:
    order = Order.objects.filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not order:
        return ''

    order.is_completed = True

    Product.objects.filter(
        order=order
    ).update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available'),
        )
    )
    order.save()

    return f'Order has been completed!'


# # Profiles
#
# 1.	Adam Smith: A customer residing at 123 Main St, Springfield, with an active profile. Contactable via email (adam.smith@example.com) and phone (123456789).
# 2.	Susan James: A customer residing at 456 Elm St, Metropolis, with an active profile. Contactable via email (susan.james@example.com) and phone (987654321).
#
# # Products
#
# 1.	Desk M: A medium-sized office desk priced at $150.00. Currently, 10 units are in stock and available for sale.
# 2.	Display DL: A 24-inch HD display priced at $200.00. Five units are in stock and available for sale.
# 3.	Printer Br PM: A high-speed printer priced at $300.00. Only three units are in stock and available for sale.
#
# # Orders
#
# 1.	Order 1: Made by Adam Smith, contains Desk M and Display DL, totaling $350.00. This order is not yet completed.
# 2.	Order 2: Made by Adam Smith, contains Printer Br PM, totaling $300.00. This order is completed.
# 3.	Order 3: Made by Adam Smith, a comprehensive order with Desk M, Display DL, and Printer Br PM, totaling $650.00. This order is not yet completed.
# 4.	Order 4: Made by Susan James, contains Desk M and Printer Br PM, totaling $450.00. This order is not yet completed.

# print(Profile.objects.get_regular_customers())
#
# print(get_profiles('Co'))
#
# print(get_profiles('9zz'))
#
# print(get_loyal_profiles())
#
# print(get_last_sold_products())
#
# print(get_top_products())
#
# print(apply_discounts())
#
# print(complete_order())