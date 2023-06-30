from django.contrib.auth.models import User
from django.db import models

PLASTIC_COLORS = [
    ('Stickerless', 'Stickerless'),
    ('Black', 'Black'),
    ('Green', 'Green'),
    ('White', 'White'),
]

ITEM_TYPE = [
    ('Puzzle', 'Puzzle'),
    ('Accessory', 'Accessory')
]


class Category(models.Model):
    category_value = models.CharField(max_length=30, null=True, blank=False)
    category_for = models.CharField(max_length=10, choices=ITEM_TYPE)
    image_url = models.URLField(null=True, blank=False)

    def __str__(self):
        return self.category_value


class EmployeeSession(models.Model):
    active_session = models.BooleanField(default=True, null=True, blank=False)
    date_time_created = models.DateTimeField(auto_now_add=True)

    # FKs
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}\'s session'


class Item(models.Model):
    name = models.CharField(max_length=100, null=True, blank=False)
    brand = models.CharField(max_length=25, null=True, blank=False)
    price = models.FloatField(null=True, blank=False)
    description = models.TextField(null=True, blank=False)
    quantity = models.IntegerField(null=True, blank=False)
    date_time_added = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=False)

    # FKs
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    employee_session = models.ForeignKey(EmployeeSession, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name


class OnPromotion(models.Model):
    discounted_price = models.FloatField(null=True, blank=False)

    # FKs
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item)


class Puzzle(Item):
    plastic_color = models.CharField(max_length=25, choices=PLASTIC_COLORS)


class Accessory(Item):
    pass


class ShoppingCart(models.Model):
    checked_out = models.BooleanField(default=False, null=True, blank=False)
    date_time_checked_out = models.DateTimeField(null=True, blank=True)

    # FKs
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class LubeService(models.Model):
    lube_type = models.CharField(max_length=50, null=True, blank=False)
    price = models.FloatField(null=True, blank=False)

    def __str__(self):
        return self.lube_type


class ItemOrder(models.Model):
    quantity = models.IntegerField(null=True, blank=False)
    shipping_price = models.FloatField(null=True, blank=False)

    # FKs
    lube_service = models.ForeignKey(LubeService, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='order_items')
