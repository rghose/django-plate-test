from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.shortcuts import render

from django.utils import timezone

from client.models import InvoiceDocument
import hashlib
import datetime

class InvoiceConstants:
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DIGITIZED = "complete"
    ALL_STATUS = [ STATUS_IN_PROGRESS, STATUS_DIGITIZED ]

class Invoice(View):

    @staticmethod
    def process_in_memory_file(file_in_memory):
        """
        do - stuff
        """
        file_content = file_in_memory.read()
        hash_object = hashlib.sha1(file_content)
        sha1_string = hash_object.hexdigest()
        current_timestamp = datetime.datetime.now(tz=timezone.utc).__str__()
        doc = InvoiceDocument(document_content=file_content, document_sha1=sha1_string, created_at=current_timestamp)
        doc.save()
        return sha1_string

    def get(self, request, *args, **kwargs):
        return HttpResponse(render(request, 'index.html', {"source": "client"}))

    def post(self, request, *args, **kwargs):
        result = Invoice.process_in_memory_file(request.FILES['file'])
        return JsonResponse({"document": result})
