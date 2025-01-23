from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Works)
admin.site.register(Category)
admin.site.register(Vehicles)
admin.site.register(User)
admin.site.register(RentTransaction)
admin.site.register(Review)