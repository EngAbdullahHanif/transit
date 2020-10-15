from django.forms import ModelForm
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Consignee, Commissionaire, BillofLading, FareBill, Recive, Account


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
            'container_weight',
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
            'rent',
            'farebill_date',
            'porterage_expenses',
            'invoice_copy',
            'commission_fee',
            'custom_expenses',
        ]


class ConsigneeForm(ModelForm):
    class Meta():
        model = Consignee
        fields = [
            'name',
            'phone_number',
        ]


class CommissionaireForm(ModelForm):
    class Meta():
        model = Commissionaire
        fields = [
            'name',
        ]


class ReciveForm(ModelForm):
    class Meta():
        model = Recive
        fields = [
            'i_number',
            'taliban_expenses',
            'eslam_qala_expenses',
            'bascol_expenses',
        ]


class AccountModelForm(BSModalModelForm):
    recieve_date = forms.DateField(
        error_messages={
            'invalid': 'لطفا به فارمت DD/MM/YYYY تاریخ وارد کنید.'},
        widget=forms.TextInput(
            attrs={'type': 'date'}),
        label='تاریخ رسید '
    )

    class Meta:
        model = Account
        fields = ['consignee', 'recieve_date', 'amount']
        error_messages = {
            'consignee': {'required': 'مشتری الزامی میباشد'},
            'amount': {
                'required': 'مقدار الزامی میباشد.',
                'min_vlaue': 'مقدار باید صفر یا از صفر بزرکتر باشد'}
        }
