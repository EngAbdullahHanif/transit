from django.contrib import admin

from .models import Consignee, Commissionaire, BillofLading, FareBill, Driver, Company, Recieve

admin.site.register(Consignee)
admin.site.register(Commissionaire)
admin.site.register(BillofLading)
admin.site.register(FareBill)
admin.site.register(Recieve)
admin.site.register(Driver)
admin.site.register(Company)
