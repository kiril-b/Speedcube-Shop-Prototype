import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .view_utils import *
from .forms import *


def home(request):
    categories = Category.objects.all()
    items_on_promotion = OnPromotion.objects.all()

    context = dict(
        categories=categories,
        items_on_promotion=items_on_promotion
    )
    return render(request, 'home.html', context)


def items_in_category(request, category):
    categories = Category.objects.all()
    items = Item.objects.filter(category__category_value=category, quantity__gt=0).all()

    if request.method == 'POST':
        min_price = request.POST['min'] if request.POST['min'] != '' else 0
        max_price = request.POST['max'] if request.POST['max'] != '' else 10000
        items = items.filter(price__gte=min_price, price__lte=max_price)

        if 'brand' in request.POST.keys():
            items = items.filter(brand__in=request.POST.getlist('brand'))

        if 'plastic_color' in request.POST.keys():
            puzzle_ids = Puzzle.objects.filter(plastic_color__in=request.POST.getlist('plastic_color')).values_list(
                'id', flat=True)
            items = items.filter(id__in=puzzle_ids)

        if 'search' in request.POST.keys():
            items = items.filter(name__icontains=request.POST['search'])

        if 'sort_by' in request.POST.keys():
            sign = '-' if 'sort_direction' in request.POST.keys() else ''
            sort_by_attribute = sign + request.POST['sort_by']
            items = items.order_by(sort_by_attribute)

    context = dict(
        category_name=category,
        categories=categories,
        items=items,
        puzzle_item=is_puzzle_instance(category),
        brands=get_brands(category),
        plastic_colors=get_plastic_colors(category)
    )
    return render(request, 'items_in_category.html', context)


def item_details(request, category, item_id):
    categories = Category.objects.all()

    item = fetch_item(category, item_id)
    lube_services = LubeService.objects.all().order_by('price')

    context = dict(
        category_name=category,
        categories=categories,
        item=item,
        puzzle_item=is_puzzle_instance(category),
        lube_serviecs=lube_services
    )
    return render(request, 'item_details.html', context)


@login_required(login_url='home')
def shopping_cart(request):
    cart, created = ShoppingCart.objects.get_or_create(user=request.user, checked_out=False)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        item_id = request.POST.get('item_id')
        shipping_price = float(request.POST.get('shipping'))

        item = Item.objects.get(id=item_id)

        lube_service = None
        if 'lube_service' in request.POST.keys():
            lube_service_id = request.POST.get('lube_service')
            lube_service = LubeService.objects.get(id=lube_service_id)

        quantity = update_quantity(item, quantity, 'subtract')

        ItemOrder.objects.create(
            quantity=quantity,
            shipping_price=shipping_price,
            lube_service=lube_service,
            item=item,
            shopping_cart=cart
        )
        return redirect('shopping_cart')

    total_shipping_price = calculate_shipping(cart)
    subtotal_price = calculate_subtotal(cart)

    categories = Category.objects.all()
    context = dict(
        categories=categories,
        order_items=cart.order_items.all(),
        shipping=round(total_shipping_price, 2),
        subtotal=round(subtotal_price, 2),
        total=round(total_shipping_price + subtotal_price, 2)
    )

    return render(request, 'shopping_cart.html', context)


def delete_order_item(request, order_item_id):
    order_item = ItemOrder.objects.get(id=order_item_id)
    item = order_item.item
    update_quantity(item, order_item.quantity, 'add')
    order_item.delete()
    return redirect('shopping_cart')


def checkout(request):
    categories = Category.objects.all()
    cart_id = request.POST.get('cart_id')

    ShoppingCart.objects.filter(id=cart_id).update(checked_out=True, date_time_checked_out=datetime.datetime.now())

    context = dict(categories=categories)
    return render(request, 'checkout.html', context)


@login_required(login_url='home')
def purchase_history(request):
    categories = Category.objects.all()
    shopping_carts = ShoppingCart.objects.filter(user=request.user, checked_out=True).order_by('-date_time_checked_out')

    context = dict(
        categories=categories,
        shopping_carts=shopping_carts
    )
    return render(request, 'purchase_history.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', dict(form=form))


@login_required(login_url='home')
def new_items_session(request):
    categories = Category.objects.all()

    empl_session, created = EmployeeSession.objects.get_or_create(user=request.user, active_session=True)

    context = dict(
        categories=categories,
        items=empl_session.items.all()
    )
    return render(request, 'new_items_session.html', context)


def delete_item(request, item_id):
    Item.objects.filter(id=item_id).delete()
    return redirect('new_items_session')


def enter_new_item(request, item_type):
    form = PuzzleForm() if item_type == 'Puzzle' else AccessoryForm()
    categories_navbar = Category.objects.all()
    categories_item = Category.objects.filter(category_for=item_type)

    categories = Category.objects.all()
    context = dict(
        categories=categories,
        categories_navbar=categories_navbar,
        categories_item=categories_item,
        form=form,
        item_type=item_type
    )
    return render(request, 'add_product.html', context)


def submit_item(request):
    if request.method == 'POST':
        item_type = request.POST.get('item_type')
        form_data = PuzzleForm(data=request.POST) if item_type == 'Puzzle' else AccessoryForm(data=request.POST)
        if form_data.is_valid():
            item = form_data.save(commit=False)

            empl_session, created = EmployeeSession.objects.get_or_create(user=request.user, active_session=True)
            category_value = request.POST.get('category_value')
            category = Category.objects.get(category_value=category_value)

            item.employee_session = empl_session
            item.category = category

            item.save()
            return redirect('new_items_session')


def save_employee_session(request):
    EmployeeSession.objects.filter(user=request.user, active_session=True).update(active_session=False)
    return redirect('home')
