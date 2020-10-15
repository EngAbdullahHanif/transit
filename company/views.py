from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import (
    BSModalDeleteView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
)

from .models import Consignee, Commissionaire, BillofLading, FareBill, Recive, Account
from .forms import (
    BillForm, FareBillForm, ConsigneeForm, CommissionaireForm, ReciveForm, AccountModelForm,
)


def home(request):
    return render(request, 'home.html')


class BillCreateView(SuccessMessageMixin, CreateView):
    model = BillofLading
    template_name = 'company/bill_create.html'
    form_class = BillForm
    success_url = reverse_lazy('bill-create')
    success_message = 'موفقانه ثبت کردید'


class BillListView(ListView):
    # model = BillofLading
    # template_name = 'company/bills_list.html'
    # context_object_name = 'bills'
    def get(self, *args, **kwargs):
        bills = BillofLading.objects.all()
        context = {
            'bills': bills
        }
        return render(self.request, 'company/bills_list.html', context)


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
        bill = kwargs['pk']
        bill_instance = BillofLading.objects.get(id=bill)

        if form.is_valid():
            porterage_expenses = form.cleaned_data.get('porterage_expenses')
            invoice_copy = form.cleaned_data.get('invoice_copy')
            commission_fee = form.cleaned_data.get('commission_fee')
            custom_expenses = form.cleaned_data.get('custom_expenses')
            rent = form.cleaned_data.get('rent')
            # BillofLading.objects.filter()

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

    def get(self, *args, **kwargs):
        bill = kwargs['pk']
        bill_instance = BillofLading.objects.get(id=bill)

        if FareBill.objects.filter(bill=bill_instance).exists():
            messages.info(self.request, 'کرایه خط از قبل ثبت کردیده است')
            return redirect('bills-list')
        return super(FareBillCreateView, self).get(*args, **kwargs)


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


def Consignee_bills_detail(request, pk):
    consignee = Consignee.objects.get(id=pk)
    bills = BillofLading.objects.filter(consignee=consignee)
    farebills = FareBill.objects.filter(bill__consignee=consignee)

    context = {
        'consignee': consignee,
        'bills': bills,
        'farebills': farebills,
    }

    return render(request, 'company/consignee_bills.html', context)


def Consignee_account_detail(request, pk):
    consignee = Consignee.objects.get(id=pk)
    accounts = Account.objects.filter(consignee=consignee)
    farbills = FareBill.objects.filter(bill__consignee=consignee)
    recives = Recive.objects.filter(bill__consignee=consignee)

    farebill_total_amount = sum([amount.total_expenses for amount in farbills])
    recive_total_amount = sum([amount.total_expenses for amount in recives])

    last_date_tatal_remaind_amount = farebill_total_amount + recive_total_amount

    total_recived_amount = sum([account.amount for account in accounts])
    total_remaind_amount = (farebill_total_amount +
                            recive_total_amount) - total_recived_amount
    context = {
        'consignee': consignee,
        'accounts': accounts,
        'farebill_total_amount': farebill_total_amount,
        'recive_total_amount': recive_total_amount,
        'total_recived_amount': total_recived_amount,
        'total_remaind_amount': total_remaind_amount
    }

    return render(request, 'company/consignee_accounts.html', context)


def is_valid_query_param(param):
    return param != "" and param is not None


def consignee_report(request):
    consignees = Consignee.objects.all()
    accounts = Account.objects.all()
    bills = []
    if request.method == 'POST':
        consignee_name = request.POST.get('consignee')
        consignee = Consignee.objects.get(name__icontains=consignee_name)
        bills = BillofLading.objects.filter(consignee=consignee)
        # recives = {}
        # for bill in bills:
        #     recives[bill] = Recive.objects.filter(bill=bill)

        max_date = request.POST.get('max_date')
        min_date = request.POST.get('min_date')
        if is_valid_query_param(min_date):
            accounts = accounts.filter(recieve_date__gte=min_date)

        if is_valid_query_param(max_date):
            accounts = accounts.filter(recieve_date__lte=max_date)

    context = {
        'consignees': consignees,
        'bills': bills,
    }
    return render(request, 'company/consignee_report.html', context)
# class ConsigneeBillsDetailView(generic.DetailView):
#     # model = FareBill
#     # template_name = 'company/farebill_detail.html'
#     # context_object_name = 'farebill'

#     def get(self, *args, **kwargs):
#         id = kwargs['pk']
#         consignee = Consignee.objects.get(id=id)
#         bills = BillofLading.objects.filter(consignee=consignee)

#         context = {
#             'bills': bills
#         }

#         return redirect(self.request, 'company/consignee_bills.html', context)


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

    def get(self, *args, **kwargs):
        bill = kwargs['pk']
        bill_instance = BillofLading.objects.get(id=bill)

        if Recive.objects.filter(bill=bill_instance).exists():
            messages.info(self.request, 'محصول از قبل ثبت کردیده است')
            return redirect('bills-list')
        return super(ReciveCreateView, self).get(*args, **kwargs)


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


class AccountCreateView(BSModalCreateView):
    template_name = 'company/account_modal/create_account.html'
    form_class = AccountModelForm
    success_message = 'پول موفقانه پرداخت شد'
    success_url = reverse_lazy('accounts-list')

    def form_valid(self, form):
        return super().form_valid(form)


class AccountListView(generic.ListView):
    # model = Account
    # context_object_name = 'accounts'
    # template_name = 'sales/accounts.html'

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     if 'type' in self.request.GET:
    #         qs = qs.filter(book_type=int(self.request.GET['type']))
    #     return qs

    def is_valid_query_param(self, param):
        return param != "" and param is not None

    def get(self, *args, **kwargs):
        accounts = Account.objects.all()
        if self.request.method == 'GET':
            min_date = self.request.GET.get('min_date')
            max_date = self.request.GET.get('max_date')
            if self.is_valid_query_param(min_date):
                accounts = accounts.filter(recieve_date__gte=min_date)

            if self.is_valid_query_param(max_date):
                accounts = accounts.filter(recieve_date__lte=max_date)

        context = {
            'accounts': accounts
        }

        return render(self.request, 'company/accounts_list.html', context)


class AccountUpdateView(BSModalUpdateView):
    model = Account
    template_name = 'company/account_modal/update_account.html'
    form_class = AccountModelForm
    success_message = 'پول موفقانه اپدیت شد'
    success_url = reverse_lazy('accounts-list')


# class AccountReadView(BSModalReadView):
#     model = Account
#     # context_object_name = 'account'
#     template_name = 'company/account_modal/account_detail.html'


class AccountDeleteView(BSModalDeleteView):
    model = Account
    template_name = 'company/account_modal/delete_account.html'
    success_message = 'معامله موفقانه حذف شد'
    success_url = reverse_lazy('accounts-list')


def add_new_function(request):
    print("thisi si skdjf")
