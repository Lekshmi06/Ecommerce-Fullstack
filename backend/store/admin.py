from django.contrib import admin
from .models import Product,Category,CustomUser,Otp,Orders,CartItem,Review

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Otp)
admin.site.register(Orders)
admin.site.register(CartItem)
admin.site.register(Review)
