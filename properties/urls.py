from django.urls import path

from .views import ItemCreateView, ItemListView, ItemUpdateView, ItemDeleteView


urlpatterns = [
    path('', ItemListView.as_view(), name="property-items-list"),
    path('item/', ItemCreateView.as_view(), name="property-item-create"),
    path('item/<int:pk>/update', ItemUpdateView.as_view(),
         name="property-item-update"),
    path('item/<int:pk>/delete', ItemDeleteView.as_view(),
         name="property-item-delete"),
]
