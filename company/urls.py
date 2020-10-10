from django.urls import path

from company.views import(
    home, BillCreateView, BillListView, BillUpdateView, BillDeleteView, BillDetailView,
    FareBillCreateView, FareBillListView, FareBillUpdateView, FareBillDeleteView, ConsigneeCreateView, ConsigneeListView, ConsigneeUpdateView, ConsigneeDeleteView
)

urlpatterns = [
    path('', home, name='home'),
    path('bill', BillCreateView.as_view(), name='bill-create'),
    path('bills', BillListView.as_view(), name='bills-list'),
    path('bill/<int:pk>/update', BillUpdateView.as_view(), name='bill-update'),
    path('bill/<int:pk>/delete', BillDeleteView.as_view(), name='bill-delete'),
    path('bill/<int:pk>', BillDetailView.as_view(), name='bill-detail'),
    path('bill/<int:pk>/farebillcreate',
         FareBillCreateView.as_view(), name='fare-bill-create'),
    path('farebills', FareBillListView.as_view(), name='farebills-list'),
    path('farebill/<int:pk>/update',
         FareBillUpdateView.as_view(), name='farebill-update'),
    path('farebill/<int:pk>/delete',
         FareBillDeleteView.as_view(), name='farebill-delete'),
    path('consignee/', ConsigneeCreateView.as_view(), name='consignee-create'),
    path('consignees', ConsigneeListView.as_view(), name='consignees-list'),
    path('consignee/<int:pk>/update', ConsigneeUpdateView.as_view(),
         name='consignee-update'),
    path('consignee/<int:pk>', ConsigneeDeleteView.as_view(),
         name='consignee-delete'),




]
