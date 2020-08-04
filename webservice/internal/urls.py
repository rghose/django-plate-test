from django.urls import path
from django.conf.urls import url

from .view.invoice_manager import InvoiceManager

urlpatterns = [
    url('invoice', InvoiceManager.as_view(), name='invoice_manager'),
]
