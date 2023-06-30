from .models import *


def is_puzzle_instance(category):
    curr_category = Category.objects.filter(category_value=category).first().category_for
    return curr_category == 'Puzzle'


def get_brands(category):
    if is_puzzle_instance(category):
        return Puzzle.objects.values_list('brand', flat=True).distinct()
    return Accessory.objects.values_list('brand', flat=True).distinct()


def get_plastic_colors(category):
    if is_puzzle_instance(category):
        return Puzzle.objects.values_list('plastic_color', flat=True).distinct()
    return None


def fetch_item(category, item_id):
    if is_puzzle_instance(category):
        return Puzzle.objects.get(id=item_id)
    return Accessory.objects.get(id=item_id)


def update_quantity(item, quantity, action):
    if action == 'subtract':
        quantity = quantity if quantity <= item.quantity else 0
        item.quantity = item.quantity - quantity
    elif action == 'add':
        item.quantity = item.quantity + quantity
    else:
        raise Exception('undefined action in update_quantity')
    item.save()
    return quantity


def calculate_shipping(cart):
    order_items = cart.order_items.all()
    return sum(o_item.shipping_price for o_item in order_items)


def calculate_subtotal(cart):
    order_items = cart.order_items.all()
    sum_ = 0
    for o_item in order_items:
        lube_service_price = o_item.lube_service.price if o_item.lube_service else 0
        sum_ += (o_item.item.price + lube_service_price) * o_item.quantity

    return sum_
