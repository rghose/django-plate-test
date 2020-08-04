from django.views.generic import View
from django.utils import timezone
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest

from client.models import InvoiceDocument, DigitizedInvoice
from client.view.invoice import InvoiceConstants

import json
import datetime


class InvoiceManager(View):
    @staticmethod
    def params_from_body(raw_data: str):
        req_data = json.loads(raw_data)
        if "id" not in req_data or "data" not in req_data:
            raise "Missing: id or data"
        status = InvoiceConstants.STATUS_IN_PROGRESS
        if "status" in req_data and req_data["status"] in InvoiceConstants.ALL_STATUS:
            status = req_data["status"]
        invoice_sha1 = req_data["id"]
        data = req_data["data"]
        return (invoice_sha1, data, status)


    def get(self, request, *args, **kwargs):
        return HttpResponse(render(request, 'all_documents.html', {"data": InvoiceDocument.objects.all()}))

    def put(self, request, *args, **kwargs):
        """
        This API expects the request to have the data in JSON format
        Example:
        curl -X PUT "http://localhost:8000/internal/invoice" --data 
        "{\"id\":\"828287ad8339773731b94668d792983caab3d805\",\"data\":{\"invoice\":\"T13209\"},\"status\":\"complete\"}
        """
        try:
            invoice_sha1, data, status = InvoiceManager.params_from_body(request.body)
        except Exception as e:
            return HttpResponseBadRequest(e)

        q_obj = InvoiceDocument.objects.filter(document_sha1=invoice_sha1)
        if len(q_obj) == 0:
            return HttpResponseNotFound("no such document %s" % invoice_sha1)
        current_timestamp = datetime.datetime.now(tz=timezone.utc)
        doc_row = q_obj[0]
        doc_row.status = status
        di = DigitizedInvoice(document_sha1=doc_row, data_json=data, created_at=current_timestamp)
        # do atomic saves for databases that support it - sqlite does not support
        # and will ignore this.
        with transaction.atomic():
            doc_row.save()
            di.save()
        return HttpResponse("OK")
