from django.contrib import admin
from .models import *


class PuzzleAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'quantity', 'date_time_added']


class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'quantity', 'date_time_added']


class EmployeeSessionAdmin(admin.ModelAdmin):
    list_display = ['active_session', 'date_time_created', 'user']


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'checked_out', 'date_time_checked_out']


admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Category)
admin.site.register(OnPromotion)
admin.site.register(ItemOrder)
admin.site.register(LubeService)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(EmployeeSession, EmployeeSessionAdmin)
