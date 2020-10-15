from django.urls import path

from .views import ItemCreateView, ItemListView, ItemUpdateView, ItemDeleteView, expenses_report


urlpatterns = [
    path('', ItemListView.as_view(), name="items-list"),
    path('item/', ItemCreateView.as_view(), name="item-create"),
    path('item/<int:pk>/update', ItemUpdateView.as_view(), name="item-update"),
    path('item/<int:pk>/delete', ItemDeleteView.as_view(), name="item-delete"),
    path('report/', expenses_report, name='expenses-report')
]
