from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from bootstrap_modal_forms.generic import BSModalDeleteView
from django.db.models import Avg, Max, Sum

from .models import Item


class ItemListView(ListView):
    model = Item
    template_name = "expenses/items_list.html"
    context_object_name = 'items'


class ItemCreateView(SuccessMessageMixin, CreateView):
    model = Item
    template_name = "expenses/item_create.html"
    fields = ['description', 'price', 'purchase_date']
    context_object_name = 'form'
    success_message = 'موفقانه ثبت کردید'
    success_url = reverse_lazy('item-create')


class ItemUpdateView(SuccessMessageMixin, UpdateView):
    model = Item
    template_name = "expenses/item_create.html"
    fields = ['description', 'price', 'purchase_date']
    context_object_name = 'form'
    success_message = 'موفقانه اپدیت کردید'
    success_url = reverse_lazy('items-list')


class ItemDeleteView(BSModalDeleteView):
    model = Item
    template_name = 'expenses/item_delete.html'
    success_message = 'موفقانه حذف شد'
    success_url = reverse_lazy('items-list')


def expenses_report(request):
    total_amount = Item.objects.all().aggregate(Sum('price'))

    # * Monthly Report
    date_list = Item.objects.filter(
        purchase_date__year=2020).dates('purchase_date', 'month')

    monthly_total_amount = []
    for months in date_list:
        monthly_total_amount.append(Item.objects.filter(purchase_date__year='2020').filter(
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

    print('=================================')
    print(anual_amount)
    print('=================================')

    context = {
        'monthly_amount': monthly_amount,
        'anual_amount': anual_amount
    }

    return render(request, 'expenses/report.html', context)
