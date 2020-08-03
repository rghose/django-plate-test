from django.shortcuts import render
from django.db import transaction

import json
import datetime
# Create your views here.
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from client.models import InvoiceDocument, DigitizedInvoice
from client.view.invoice import InvoiceConstants

def get_all_docs(request):
    return HttpResponse(render(request, 'all_documents.html', {"data": InvoiceDocument.objects.all()}))

def update_invoice(request):
    if request.method != "PUT":
        return HttpResponseNotAllowed("method not allowed")
    req_data = json.loads(request.body)
    if "id" not in req_data or "data" not in req_data:
        return HttpResponseBadRequest("bad format")
    status = InvoiceConstants.STATUS_IN_PROGRESS
    if "status" in req_data and req_data["status"] in InvoiceConstants.ALL_STATUS:
        status = req_data["status"]
    invoice_sha1 = req_data["id"]
    data = req_data["data"]
    q_obj = InvoiceDocument.objects.filter(document_sha1=invoice_sha1)
    if len(q_obj) == 0:
        return HttpResponseNotFound("no such document %s" % invoice_sha1)
    current_timestamp = datetime.datetime.now().__str__()
    doc_row = q_obj[0]
    doc_row.status = status
    di = DigitizedInvoice(document_sha1=doc_row, data_json=data, created_at=current_timestamp)
    with transaction.atomic():
        di.save()
        doc_row.save()
    return HttpResponse("OK")
