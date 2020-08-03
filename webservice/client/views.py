from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from .view.invoice import InvoiceConstants

from client.models import InvoiceDocument, DigitizedInvoice

def get_invoice_status(request, invoice_sha1: str) -> JsonResponse:
    query_result = InvoiceDocument.objects.filter(document_sha1=invoice_sha1)
    if len(query_result) == 0:
        return HttpResponseNotFound("no such document %s" % invoice_sha1)
    status = query_result[0].status
    response = { "document": invoice_sha1, "status": status }
    if status == InvoiceConstants.STATUS_DIGITIZED:
        latest_result = DigitizedInvoice.objects.filter(document_sha1=invoice_sha1).order_by('-created_at')[0]
        response["result"] = latest_result.data_json
    return JsonResponse(response)
