from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from . models import (
    Customer,
    Payment,
    Product,
    Cart,
    OrderPlaced
)
# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']

@admin.register(Product) 
class ProductModelAdmin(admin.ModelAdmin): 
    list_display = ['id','title','selling_price','discounted_price','description','category','product_image'] 


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','customer_info','product','product_info','quantity','ordered_date','status']

    def customer_info(self,obj):
        link = reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)

    def product_info(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','product_info','payment_status']

    def customer_info(self,obj):
        link = reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)

    def product_info(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
