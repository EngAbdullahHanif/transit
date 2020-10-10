from django.forms import ModelForm
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Consignee, Commissionaire, BillofLading, FareBill


class BillForm(ModelForm):
    class Meta():
        model = BillofLading
        fields = [
            'consignee',
            'commissionaire',
            'bill_number',
            'check_number',
            'arrival_date',
            'lading_date',
            'exit_date',
            'origin_custom',
            'destination_custom',
            'act_cmr',
            'container_number',
            'empty_number',
            'commodity',
            'quantity',
            'net_weight',
            'conatiner_weight',
            'licens_number',
            'b_l_number',
            'driver',
            'driver_father',
            'truck_number',
            'transport',
            'asab_shasi',
            'truck_shasi',
            'tin_jawaz',
        ]


# class FareBillForm(BSModalModelForm):
#     class Meta():
#         model = FareBill
#         fields = [
#             'porterage_expenses',
#             'invoice_copy',
#             'commission_fee',
#             'custom_expenses'
#         ]


class FareBillForm(ModelForm):
    class Meta():
        model = FareBill
        fields = [
            'porterage_expenses',
            'invoice_copy',
            'commission_fee',
            'custom_expenses',
            'rent'
        ]


class ConsigneeForm(ModelForm):
    class Meta():
        model = Consignee
        fields = [
            'name',
            'phone_number',
        ]
