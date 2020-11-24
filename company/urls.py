from django.urls import path

from company.views import(
    HomeView, BillCreateView, BillListView, BillUpdateView, BillDeleteView, BillDetailView,
    FareBillCreateView, FareBillListView, FareBillDetailView, FareBillUpdateView, FareBillDeleteView,
    ConsigneeCreateView, ConsigneeListView, ConsigneeUpdateView, ConsigneeDeleteView, Consignee_bills_detail, Consignee_account_detail, ConsigneeReportView,
    CommissionaireCreateView, CommissionaireListView, CommissionaireUpdateView, CommissionaireDeleteView,
    RecieveCreateView, RecieveListView, RecieveUpdateView, RecieveDeleteView,
    AccountCreateView, AccountDeleteView, AccountListView, AccountUpdateView, AccountReport,
    DriverListView, DriverUpdateView, DriverDeleteView, DriverFareBillsListView, DriverCreateView,
    DoseBolaqCreateView, DoseBolaqListView, DoseBolaqUpdateView, DoseBolaqDeleteView, dosebolaq_report,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('bill', BillCreateView.as_view(), name='bill-create'),
    path('bills', BillListView.as_view(), name='bills-list'),
    path('bill/<int:pk>/update', BillUpdateView.as_view(), name='bill-update'),
    path('bill/<int:pk>/delete', BillDeleteView.as_view(), name='bill-delete'),
    path('bill/<int:pk>', BillDetailView.as_view(), name='bill-detail'),


    path('bill/<int:pk>/farebillcreate',
         FareBillCreateView.as_view(), name='farebill-create'),
    path('farebills', FareBillListView.as_view(), name='farebills-list'),
    path('farebill/<int:pk>', FareBillDetailView.as_view(), name='farebill-detail'),
    path('farebill/<int:pk>/update',
         FareBillUpdateView.as_view(), name='farebill-update'),
    path('farebill/<int:pk>/delete',
         FareBillDeleteView.as_view(), name='farebill-delete'),


    path('consignee/', ConsigneeCreateView.as_view(), name='consignee-create'),
    path('consignees', ConsigneeListView.as_view(), name='consignees-list'),
    path('consignee/<int:pk>/update', ConsigneeUpdateView.as_view(),
         name='consignee-update'),
    path('consignee/<int:pk>/delete', ConsigneeDeleteView.as_view(),
         name='consignee-delete'),
    path('consignee/<int:pk>/bills', Consignee_bills_detail,
         name='consignee-bills-detail'),
    path('consignee/<int:pk>/account', Consignee_account_detail,
         name='consignee-accounts-detail'),

    path('consignee/report', ConsigneeReportView.as_view(), name='consignee-report'),


    path('commissionaire', CommissionaireCreateView.as_view(),
         name='commissionaire-create'),
    path('commissionaires', CommissionaireListView.as_view(),
         name='commissionaires-list'),
    path('commissionaire/<int:pk>/update', CommissionaireUpdateView.as_view(),
         name='commissionaire-update'),
    path('commissionaire/<int:pk>/delete', CommissionaireDeleteView.as_view(),
         name='commissionaire-delete'),


    path('recieves', RecieveListView.as_view(), name='recieves-list'),
    path('bill/<int:pk>/recieve', RecieveCreateView.as_view(), name='recieve-create'),
    path('recieve/<int:pk>/update',
         RecieveUpdateView.as_view(), name='recieve-update'),
    path('recieve/<int:pk>/delete',
         RecieveDeleteView.as_view(), name='recieve-delete'),


    path('accounts/', AccountListView.as_view(), name='accounts-list'),
    path('account/create', AccountCreateView.as_view(), name='account-create'),
    path('accounts/<int:pk>/update',
         AccountUpdateView.as_view(), name='account-update'),
    path('accounts/<int:pk>/delete',
         AccountDeleteView.as_view(), name='account-delete'),
    path('accounts/report/', AccountReport.as_view(), name='accounts-report'),


    path('drivers', DriverListView.as_view(), name='drivers-list'),
    path('driver', DriverCreateView.as_view(), name='driver-create'),
    path('driver/<int:pk>/update', DriverUpdateView.as_view(), name='driver-update'),
    path('driver/<int:pk>/delete', DriverDeleteView.as_view(), name='driver-delete'),
    path('driver/<int:pk>/farebills',
         DriverFareBillsListView.as_view(), name='driver-farebills-list'),

    path('dosebolaq', DoseBolaqCreateView.as_view(),
         name='dosebolaq-create'),
    path('dosebolaqs', DoseBolaqListView.as_view(),
         name='dosebolaqs-list'),
    path('dosebolaq/<int:pk>/update', DoseBolaqUpdateView.as_view(),
         name='dosebolaq-update'),
    path('dosebolaq/<int:pk>/delete', DoseBolaqDeleteView.as_view(),
         name='dosebolaq-delete'),
    path('dosebolaq/report', dosebolaq_report,
         name='dosebolaq-report'),

]
