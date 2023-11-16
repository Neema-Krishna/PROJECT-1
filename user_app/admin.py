from django.contrib import admin
from user_app.models import MyUser_registration,Vehicle,Cart,Vehicle_name,Brand,Booking,Query,Information

# Register your models here.
admin.site.register(MyUser_registration)
admin.site.register(Vehicle)
admin.site.register(Cart)
admin.site.register(Vehicle_name)
admin.site.register(Brand)
admin.site.register(Booking)
admin.site.register(Query)
admin.site.register(Information)
