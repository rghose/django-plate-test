from django.urls import path
from django.conf.urls import url

from . import views

from .view.invoice import Invoice

urlpatterns = [
    url(r'^invoice/$', Invoice.as_view(), name='invoice'),
    path('invoice/<str:invoice_sha1>/', views.get_invoice_status),
]

