from django.contrib import admin

from .models import Consignee, Commissionaire, BillofLading, FareBill

admin.site.register(Consignee)
admin.site.register(Commissionaire)
admin.site.register(BillofLading)
admin.site.register(FareBill)
