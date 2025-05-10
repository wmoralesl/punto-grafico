from django.contrib import admin

# Register your models here.
from .models import Order, OrderLine

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]

admin.site.register(Order, OrderAdmin)