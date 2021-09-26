from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Stock)
admin.site.register(Product)
admin.site.register(Partner)
admin.site.register(Deal)
admin.site.register(DealType)
admin.site.register(DealProduct)