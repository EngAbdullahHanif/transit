from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from bootstrap_modal_forms.generic import BSModalDeleteView
from django.db.models import Avg, Max, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum
from django.db.models.functions import ExtractWeekDay

from .models import Item


class ItemListView(ListView):
    model = Item
    template_name = "expenses/items_list.html"
    context_object_name = 'items'


class ItemCreateView(SuccessMessageMixin, CreateView):
    model = Item
    template_name = "expenses/item_create.html"
    fields = ['description', 'price', 'purchase_date', 'consumer', 'bill']
    context_object_name = 'form'
    success_message = 'موفقانه ثبت کردید'
    success_url = reverse_lazy('item-create')


class ItemUpdateView(SuccessMessageMixin, UpdateView):
    model = Item
    template_name = "expenses/item_create.html"
    fields = ['description', 'price', 'purchase_date', 'consumer', 'bill']
    context_object_name = 'form'
    success_message = 'موفقانه اپدیت کردید'
    success_url = reverse_lazy('items-list')


class ItemDeleteView(BSModalDeleteView):
    model = Item
    template_name = 'expenses/item_delete.html'
    success_message = 'موفقانه حذف شد'
    success_url = reverse_lazy('items-list')


def expenses_report(request):
    current_year = timezone.now().year
    weekDays = ("دوشنبه", "سه شنبه", "چهار شنبه",
                "پنج شنبه", "جمعه", "شنبه", "یک شنبه")

    # * Todays Report
    current_date = datetime.now().date()
    current_day = weekDays[current_date.weekday()]
    today_amount = Item.objects.filter(
        purchase_date=current_date).aggregate(expends=Sum('price'))

    # * Weekly Report
    dt = datetime.now()
    start = (dt - timedelta(days=(dt.weekday() + 2) % 7)) - timedelta(days=7)
    end = (start + timedelta(days=6))
    date_list = Item.objects.filter(
        purchase_date__range=(start.date(), end.date())).annotate(day=ExtractWeekDay('purchase_date')).values('day').annotate(expends=Sum('price'))

    weekl_amount = {}
    weekDays = ("شنبه", "یک شنبه", "دوشنبه",
                "سه شنبه", "چهار شنبه", "پنج شنبه", "جمعه")
    for day in date_list:
        weekl_amount[weekDays[day['day']]] = day['expends']

    # * Monthly Report
    date_list = Item.objects.filter(
        purchase_date__year=current_year).dates('purchase_date', 'month')

    monthly_total_amount = []
    for months in date_list:
        monthly_total_amount.append(Item.objects.filter(purchase_date__year=current_year).filter(
            purchase_date__month=months.month).aggregate(Sum('price')))

    monthly_amount = {}
    num = 0
    for months in date_list:
        monthly_amount[months.month] = monthly_total_amount[num]
        num += 1

    # * Anual Report
    date_list = Item.objects.all().dates('purchase_date', 'year')

    anual_total_amount = []
    for years in date_list:
        anual_total_amount.append(Item.objects.filter(
            purchase_date__year=years.year).aggregate(Sum('price')))

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
