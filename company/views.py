from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, F
from django.db.models.functions import ExtractWeekDay
from django.core.exceptions import ObjectDoesNotExist


from bootstrap_modal_forms.generic import (
    BSModalDeleteView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
)

from .models import (
    Consignee, Commissionaire, BillofLading, FareBill, Recieve, Account, Driver, DoseBolaq
)

from .forms import (
    BillForm, FareBillForm, ConsigneeForm, CommissionaireForm, RecieveForm, AccountModelForm,
    DriverModelForm, DriverForm, DoseBolaqForm,
)


# def home(request):
#     return render(request, 'home.html')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


# * Bill
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


# * Farebill
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
            received = form.cleaned_data.get('received')
            # BillofLading.objects.filter()

            farebill = FareBill(
                bill=bill_instance,
                porterage_expenses=porterage_expenses,
                invoice_copy=invoice_copy,
                commission_fee=commission_fee,
                custom_expenses=custom_expenses,
                rent=rent,
                received=received,
            )
            farebill.save()
            messages.success(self.request, 'کرایه خط موفقانه ثبت کردید')
            return redirect('bills-list')

        messages.success(self.request, 'کرایه خط  ثبت نه گردید')
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


# * Consignee
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
    recieves = BillofLading.objects.filter(consignee=consignee)

    farebill_total_amount = sum([amount.total_expenses for amount in farbills])
    # last_date_tatal_remaind_amount = farebill_total_amount + recieve_total_amount

    recieve_total_amount = 0
    for re in recieves:
        if re.recieve is not None:
            print(re.recieve.total_expenses)
            recieve_total_amount = recieve_total_amount + re.recieve.total_expenses

    total_recieved_amount = sum([account.amount for account in accounts])
    total_remaind_amount = recieve_total_amount - total_recieved_amount

    context = {
        'consignee': consignee,
        'accounts': accounts,
        'farebill_total_amount': farebill_total_amount,
        'recieve_total_amount': recieve_total_amount,
        'total_recieved_amount': total_recieved_amount,
        'total_remaind_amount': total_remaind_amount
    }
    return render(request, 'company/consignee_accounts.html', context)


def is_valid_query_param(param):
    return param != "" and param is not None


class ConsigneeReportView(TemplateView):
    def get(self, *args, **kwargs):
        consignees = Consignee.objects.all()
        bills = []
        if self.request.method == 'POST':
            consignee_name = request.POST.get('consignee')
            consignee = Consignee.objects.get(name__icontains=consignee_name)
            bills = BillofLading.objects.filter(consignee=consignee)

        context = {
            # 'consignee': consignee,
            'consignees': consignees,
            'bills': bills,
        }
        return render(self.request, 'company/consignee_report.html', context)

    def post(self, *args, **kwargs):
        consignees = Consignee.objects.all()
        consignee_name = self.request.POST.get('consignee')
        consignee = Consignee.objects.get(name__icontains=consignee_name)
        bills = BillofLading.objects.filter(consignee=consignee)

        commodity = self.request.POST.get('commodity')
        max_date = self.request.POST.get('max_date')
        min_date = self.request.POST.get('min_date')

        if is_valid_query_param(commodity):
            bills = bills.filter(commodity__icontains=commodity)
        if is_valid_query_param(min_date):
            bills = bills.filter(exit_date__gte=min_date)
        if is_valid_query_param(max_date):
            bills = bills.filter(exit_date__lte=max_date)

        taliban_expenses = 0
        eslam_qala_expenses = 0
        bascol_expenses = 0
        for bill in bills:
            if bill.recieve is not None:
                taliban_expenses = taliban_expenses + bill.recieve.taliban_expenses
                eslam_qala_expenses = eslam_qala_expenses + bill.recieve.eslam_qala_expenses
                bascol_expenses = bascol_expenses + bill.recieve.bascol_expenses

        total_expenses = taliban_expenses + eslam_qala_expenses + bascol_expenses

        context = {
            'consignees': consignees,
            'bills': bills,
            'taliban_expenses': taliban_expenses,
            'eslam_qala_expenses': eslam_qala_expenses,
            'bascol_expenses': bascol_expenses,
            'total_expenses': total_expenses,
        }

        return render(self.request, 'company/consignee_report.html', context)


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


# * Commissionaire
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


# * Recieve Bills
class RecieveCreateView(CreateView):
    model = Recieve
    template_name = 'company/recieve_create.html'
    form_class = RecieveForm
    success_url = reverse_lazy('recieve-create')
    success_message = 'موفقانه ثبت کردید'

    def post(self, *args, **kwargs):
        form = RecieveForm(self.request.POST)
        if form.is_valid():
            i_number = form.cleaned_data.get('i_number')
            taliban_expenses = form.cleaned_data.get('taliban_expenses')
            eslam_qala_expenses = form.cleaned_data.get('eslam_qala_expenses')
            bascol_expenses = form.cleaned_data.get('bascol_expenses')
            bill = kwargs['pk']
            bill_instance = BillofLading.objects.get(id=bill)
            recieve = Recieve(
                i_number=i_number,
                taliban_expenses=taliban_expenses,
                eslam_qala_expenses=eslam_qala_expenses,
                bascol_expenses=bascol_expenses,
            )
            # *links the Recieve paper with Bill
            recieve.save()
            bill_instance.recieve = recieve
            bill_instance.save()
            messages.success(self.request, 'محصول موفقانه ثبت کردید')
            return redirect('bills-list')

    def get(self, *args, **kwargs):
        bill = kwargs['pk']
        bill_instance = BillofLading.objects.get(id=bill)
        if bill_instance.recieve is not None:
            messages.info(self.request, 'محصول از قبل ثبت کردیده است')
            return redirect('bills-list')
        return super(RecieveCreateView, self).get(*args, **kwargs)


class RecieveListView(ListView):
    model = Recieve
    template_name = 'company/recieves_list.html'
    context_object_name = 'recieves'

    # def get(self, *args, **kwargs):
    #     bills = BillofLading.objects.all()
    #     # recieves = {}
    #     # for bill in bills:
    #     #     if bill.recieve is not None:
    #     #         recieves = bill.recieve.taliban_expenses
    #     # print(recieves)
    #     context = {
    #         'bills': bills
    # }

    # return render(self.request, 'company/recieves_list.html', context)


class RecieveUpdateView(SuccessMessageMixin, UpdateView):
    model = Recieve
    template_name = 'company/recieve_create.html'
    form_class = RecieveForm
    success_url = reverse_lazy('recieves-list')
    success_message = 'موفقانه اپدیت کردید'


class RecieveDeleteView(BSModalDeleteView):
    model = Recieve
    template_name = 'company/modals/recieve_delete.html'
    success_url = reverse_lazy('recieves-list')
    success_message = 'موفقانه حذف کردید'


class RecieveDetailView(DetailView):
    model = Recieve
    template_name = 'company/bill_detail.html'
    context_object_name = 'farebill'


# * Account
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


class AccountReport(TemplateView):
    # template_name = 'company/account_report.html'
    def get(self, *args, **kwargs):
        current_year = timezone.now().year
        weekDays = ("دوشنبه", "سه شنبه", "چهار شنبه",
                    "پنج شنبه", "جمعه", "شنبه", "یک شنبه")

        # * Todays Report
        current_date = datetime.now().date()
        current_day = weekDays[current_date.weekday()]
        today_amount = Account.objects.filter(
            recieve_date=current_date).aggregate(expends=Sum('amount'))

        # * Weekly Report
        dt = datetime.now()
        start = (dt - timedelta(days=(dt.weekday() + 2) % 7)) - \
            timedelta(days=7)
        end = (start + timedelta(days=6))
        date_list = Account.objects.filter(
            recieve_date__range=(start.date(), end.date())).annotate(day=ExtractWeekDay('recieve_date')).values('day').annotate(expends=Sum('amount'))

        weekl_amount = {}
        weekDays = ("شنبه", "یک شنبه", "دوشنبه",
                    "سه شنبه", "چهار شنبه", "پنج شنبه", "جمعه")
        for day in date_list:
            weekl_amount[weekDays[day['day']]] = day['expends']

        # * Monthly Report
        date_list = Account.objects.filter(
            recieve_date__year=current_year).dates('recieve_date', 'month')

        monthly_total_amount = []
        for months in date_list:
            monthly_total_amount.append(Account.objects.filter(recieve_date__year=current_year).filter(
                recieve_date__month=months.month).aggregate(Sum('amount')))

        monthly_amount = {}
        num = 0
        for months in date_list:
            monthly_amount[months.month] = monthly_total_amount[num]
            num += 1

        # * Anual Report
        date_list = Account.objects.all().dates('recieve_date', 'year')

        anual_total_amount = []
        for years in date_list:
            anual_total_amount.append(Account.objects.filter(
                recieve_date__year=years.year).aggregate(Sum('amount')))

        anual_amount = {}
        num = 0
        for years in date_list:
            anual_amount[years.year] = anual_total_amount[num]
            num += 1

        context = {
            'current_year': current_year,
            'current_day': current_day,
            'today_amount': today_amount,
            'weekly_amount': weekl_amount,
            'monthly_amount': monthly_amount,
            'anual_amount': anual_amount
        }
        return render(self.request, 'company/account_report.html', context)


# * Driver
class DriverCreateView(SuccessMessageMixin, CreateView):
    model = Driver
    template_name = 'company/driver_create.html'
    form_class = DriverForm
    success_url = reverse_lazy('driver-create')
    success_message = 'موفقانه ثبت کردید'


class DriverListView(ListView):
    model = Driver
    template_name = 'company/drivers_list.html'
    context_object_name = 'drivers'


class DriverUpdateView(BSModalUpdateView):
    model = Driver
    template_name = 'company/modals/update_driver.html'
    form_class = DriverModelForm
    success_message = 'دریور موفقانه اپدیت شد'
    success_url = reverse_lazy('drivers-list')


class DriverDeleteView(BSModalDeleteView):
    model = Driver
    template_name = 'company/modals/delete_driver.html'
    success_message = 'دریور موفقانه حذف شد'
    success_url = reverse_lazy('drivers-list')


class DriverFareBillsListView(ListView):

    def get(self, *args, **kwargs):
        driver_id = kwargs['pk']
        driver = Driver.objects.get(id=driver_id)
        farebills = FareBill.objects.filter(bill__driver__id=driver_id)
        total_remained = farebills.annotate(remained=(F(
            'porterage_expenses') + F('invoice_copy') + F('commission_fee') + F('custom_expenses') + F('rent')) - F('received')).aggregate(reamined=Sum('remained'))

        context = {
            'driver': driver,
            'farebills': farebills,
            'total_remianed': total_remained,
        }

        return render(self.request, 'company/driver_farebills_list.html', context)


# * Dosbolaq
class DoseBolaqCreateView(SuccessMessageMixin, CreateView):
    model = DoseBolaq
    template_name = 'company/dosebolaq_create.html'
    form_class = DoseBolaqForm
    success_url = reverse_lazy('dosebolaq-create')
    success_message = 'موفقانه ثبت کردید'


class DoseBolaqListView(ListView):
    model = DoseBolaq
    template_name = 'company/dosebolaq_list.html'
    context_object_name = 'dosebolaqs'


class DoseBolaqUpdateView(SuccessMessageMixin, UpdateView):
    model = DoseBolaq
    template_name = 'company/dosebolaq_create.html'
    form_class = DoseBolaqForm
    success_url = reverse_lazy('dose-bolaq-list')
    success_message = 'موفقانه اپدیت کردید'


class DoseBolaqDeleteView(BSModalDeleteView):
    model = DoseBolaq
    template_name = 'company/modals/dosebolaq_delete.html'
    success_url = reverse_lazy('dose-bolaq-list')
    success_message = 'موفقانه حذف کردید'


def dosebolaq_report(request):
    current_year = timezone.now().year
    weekDays = ("دوشنبه", "سه شنبه", "چهار شنبه",
                "پنج شنبه", "جمعه", "شنبه", "یک شنبه")

    # * Todays Report
    current_date = datetime.now().date()
    current_day = weekDays[current_date.weekday()]
    today_amount = DoseBolaq.objects.filter(
        recieved_date=current_date).aggregate(expends=Sum('amount'))

    # * Weekly Report
    dt = datetime.now()
    start = (dt - timedelta(days=(dt.weekday() + 2) % 7)) - timedelta(days=7)
    end = (start + timedelta(days=6))
    date_list = DoseBolaq.objects.filter(
        recieved_date__range=(start.date(), end.date())).annotate(day=ExtractWeekDay('recieved_date')).values('day').annotate(expends=Sum('amount'))

    weekl_amount = {}
    weekDays = ("شنبه", "یک شنبه", "دوشنبه",
                "سه شنبه", "چهار شنبه", "پنج شنبه", "جمعه")
    for day in date_list:
        weekl_amount[weekDays[day['day']]] = day['expends']

    # * Monthly Report
    date_list = DoseBolaq.objects.filter(
        recieved_date__year=current_year).dates('recieved_date', 'month')

    monthly_total_amount = []
    for months in date_list:
        monthly_total_amount.append(DoseBolaq.objects.filter(recieved_date__year=current_year).filter(
            recieved_date__month=months.month).aggregate(Sum('amount')))

    monthly_amount = {}
    num = 0
    for months in date_list:
        monthly_amount[months.month] = monthly_total_amount[num]
        num += 1

    # * Anual Report
    date_list = DoseBolaq.objects.all().dates('recieved_date', 'year')

    anual_total_amount = []
    for years in date_list:
        anual_total_amount.append(DoseBolaq.objects.filter(
            recieved_date__year=years.year).aggregate(Sum('amount')))

    anual_amount = {}
    num = 0
    for years in date_list:
        anual_amount[years.year] = anual_total_amount[num]
        num += 1

    context = {
        'current_year': current_year,
        'current_day': current_day,
        'today_amount': today_amount,
        'weekly_amount': weekl_amount,
        'monthly_amount': monthly_amount,
        'anual_amount': anual_amount
    }

    return render(request, 'expenses/report.html', context)
