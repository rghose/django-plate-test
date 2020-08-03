from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.get_all_docs),
    path('invoice', views.update_invoice)
]

