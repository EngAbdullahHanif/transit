from django.urls import path
from company.views import home
urlpatterns = [
    path('', home, name='home')
]
