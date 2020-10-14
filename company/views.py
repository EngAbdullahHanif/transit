from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import (
    BSModalDeleteView,
    BSModalCreateView,
)

from .models import Consignee, Commissionaire, BillofLading, FareBill, Recive
from .forms import BillForm, FareBillForm, ConsigneeForm, CommissionaireForm, ReciveForm


def home(request):
    return render(request, 'home.html')


class BillCreateView(SuccessMessageMixin, CreateView):
    model = BillofLading
    template_name = 'company/bill_create.html'
    form_class = BillForm
    success_url = reverse_lazy('bill-create')
    success_message = 'موفقانه ثبت کردید'


class BillListView(ListView):
    model = BillofLading
    template_name = 'company/bills_list.html'
    context_object_name = 'bills'


class BillUpdateView(SuccessMessageMixin, UpdateView):
    model = BillofLading
    template_name = 'company/bill_create.html'
    form_class = BillForm
    success_url = reverse_lazy('bill-create')
    success_message = 'موفقانه اپدیت کردید'


class BillDeleteView(SuccessMessageMixin, BSModalDeleteView):
    model = BillofLading
    template_name = 'company/modals/bill_delete.html'
    success_url = reverse_lazy('bills-list')
    success_message = 'موفقانه حذف کردید'


class BillDetailView(DetailView):
    model = BillofLading
    template_name = 'company/bill_detail.html'
    context_object_name = 'bill'


# !NOT WORKING
# class FareBillCreateView(BSModalCreateView):
#     # model = FareBill
#     template_name = 'company/modals/fare_bill_create.html'
#     form_class = FareBillForm
#     success_url = reverse_lazy('bills')
#     success_message = 'کرایه خط موفقانه ثبت کردید'


class FareBillCreateView(CreateView):
    model = FareBill
    template_name = 'company/fare_bill_create.html'
    form_class = FareBillForm
    success_url = reverse_lazy('bills')
    success_message = 'کرایه خط موفقانه ثبت کردید'

    def post(self, *args, **kwargs):
        form = FareBillForm(self.request.POST)
        if form.is_valid():
            porterage_expenses = form.cleaned_data.get('porterage_expenses')
            invoice_copy = form.cleaned_data.get('invoice_copy')
            commission_fee = form.cleaned_data.get('commission_fee')
            custom_expenses = form.cleaned_data.get('custom_expenses')
            rent = form.cleaned_data.get('rent')
            bill = kwargs['pk']
            bill_instance = BillofLading.objects.get(id=bill)
            farebill = FareBill(
                bill=bill_instance,
                porterage_expenses=porterage_expenses,
                invoice_copy=invoice_copy,
                commission_fee=commission_fee,
                custom_expenses=custom_expenses,
                rent=rent,
            )
            farebill.save()
            messages.success(self.request, 'کرایه خط موفقانه ثبت کردید')
            return redirect('bills-list')


class FareBillListView(ListView):
    model = FareBill
    template_name = 'company/fare_bills_list.html'
    context_object_name = 'farebills'


class FareBillUpdateView(SuccessMessageMixin, UpdateView):
    model = FareBill
    template_name = 'company/fare_bill_create.html'
    form_class = FareBillForm
    success_url = reverse_lazy('farebills-list')
    success_message = 'موفقانه اپدیت کردید'


class FareBillDeleteView(BSModalDeleteView):
    model = FareBill
    template_name = 'company/modals/farebill_delete.html'
    success_url = reverse_lazy('farebills-list')
    success_message = 'موفقانه حذف کردید'


class FareBillDetailView(DetailView):
    model = FareBill
    template_name = 'company/farebill_detail.html'
    context_object_name = 'farebill'


class ConsigneeCreateView(SuccessMessageMixin, CreateView):
    model = Consignee
    template_name = 'company/consignee_create.html'
    form_class = ConsigneeForm
    success_url = reverse_lazy('consignee-create')
    success_message = 'موفقانه ثبت کردید'


class ConsigneeListView(ListView):
    model = Consignee
    template_name = 'company/consignees_list.html'
    context_object_name = 'consignees'


class ConsigneeUpdateView(SuccessMessageMixin, UpdateView):
    model = Consignee
    template_name = 'company/consignee_create.html'
    form_class = ConsigneeForm
    success_url = reverse_lazy('consignees-list')
    success_message = 'موفقانه اپدیت کردید'


class ConsigneeDeleteView(BSModalDeleteView):
    model = Consignee
    template_name = 'company/modals/consignee_delete.html'
    success_url = reverse_lazy('consignees-list')
    success_message = 'موفقانه حذف کردید'


class ConsigneeDetailView(DetailView):
    model = FareBill
    template_name = 'company/farebill_detail.html'
    context_object_name = 'farebill'


class CommissionaireCreateView(SuccessMessageMixin, CreateView):
    model = Commissionaire
    template_name = 'company/commissionaire_create.html'
    form_class = CommissionaireForm
    success_url = reverse_lazy('commissionaire-create')
    success_message = 'موفقانه ثبت کردید'


class CommissionaireListView(ListView):
    model = Commissionaire
    template_name = 'company/commissionaires_list.html'
    context_object_name = 'commissionaires'


class CommissionaireUpdateView(SuccessMessageMixin, UpdateView):
    model = Commissionaire
    template_name = 'company/commissionaire_create.html'
    form_class = CommissionaireForm
    success_url = reverse_lazy('commissionaires-list')
    success_message = 'موفقانه اپدیت کردید'


class CommissionaireDeleteView(BSModalDeleteView):
    model = Commissionaire
    template_name = 'company/modals/commissionaire_delete.html'
    success_url = reverse_lazy('commissionaires-list')
    success_message = 'موفقانه حذف کردید'


class CommissionaireDetailView(DetailView):
    model = Commissionaire
    template_name = 'company/bill_detail.html'
    context_object_name = 'farebill'


class ReciveCreateView(CreateView):
    model = Recive
    template_name = 'company/recive_create.html'
    form_class = ReciveForm
    success_url = reverse_lazy('recive-create')
    success_message = 'موفقانه ثبت کردید'

    def post(self, *args, **kwargs):
        form = ReciveForm(self.request.POST)
        if form.is_valid():
            i_number = form.cleaned_data.get('i_number')
            taliban_expenses = form.cleaned_data.get('taliban_expenses')
            eslam_qala_expenses = form.cleaned_data.get('eslam_qala_expenses')
            bascol_expenses = form.cleaned_data.get('bascol_expenses')
            bill = kwargs['pk']
            bill_instance = BillofLading.objects.get(id=bill)
            recive = Recive(
                bill=bill_instance,
                i_number=i_number,
                taliban_expenses=taliban_expenses,
                eslam_qala_expenses=eslam_qala_expenses,
                bascol_expenses=bascol_expenses,
            )
            recive.save()
            messages.success(self.request, 'محصول موفقانه ثبت کردید')
            return redirect('bills-list')


class ReciveListView(ListView):
    model = Recive
    template_name = 'company/recives_list.html'
    context_object_name = 'recives'


class ReciveUpdateView(SuccessMessageMixin, UpdateView):
    model = Recive
    template_name = 'company/recive_create.html'
    form_class = ReciveForm
    success_url = reverse_lazy('recives-list')
    success_message = 'موفقانه اپدیت کردید'


class ReciveDeleteView(BSModalDeleteView):
    model = Recive
    template_name = 'company/modals/recive_delete.html'
    success_url = reverse_lazy('recives-list')
    success_message = 'موفقانه حذف کردید'


class ReciveDetailView(DetailView):
    model = Recive
    template_name = 'company/bill_detail.html'
    context_object_name = 'farebill'
