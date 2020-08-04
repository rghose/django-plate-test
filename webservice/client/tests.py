from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.utils import timezone

from .view.invoice import Invoice
from client.models import InvoiceDocument

SAMPLE_DATA_1 = {
    "data": "mockdata",
    "hash": "8bc86513cfd731529471437f987663669d915cf5"
}

class MockFile():
    def __init__(self, data):
        self.data = data
    def read(self):
        return self.data.encode()

class InvoiceDocumentTest(TestCase):
    def test_get_sha1(self):
        result = Invoice.process_in_memory_file(MockFile(SAMPLE_DATA_1["data"]))
        self.assertEqual(result, SAMPLE_DATA_1["hash"])
    
    def test_multiple_uploads_dont_create_duplicates(self):
        some_content = "lorem ipsum < PDF > blah"
        result1 = Invoice.process_in_memory_file(MockFile(some_content))
        result2 = Invoice.process_in_memory_file(MockFile(some_content))
        self.assertEqual(result1, result2)
        q = InvoiceDocument.objects.all()
        self.assertEqual(len(q), 1)


from django.test.client import RequestFactory
from . import views
import json

class ViewsTesting(TestCase):
    def test_get_invalid_invoice_status(self):
        rf = RequestFactory()
        get_request = rf.get('/client/invoice/invoice')
        response = views.get_invoice_status(get_request, "invoice")
        self.assertEqual(response.status_code, 404)

    def test_get_valid_invoice_status(self):
        file_id = Invoice.process_in_memory_file(MockFile(SAMPLE_DATA_1["data"]))
        rf = RequestFactory()
        get_request = rf.get('/client/invoice/' + file_id)
        response = views.get_invoice_status(get_request, file_id)
        self.assertEqual(response.status_code, 200)
        content_json = json.loads(response.content)
        self.assertEqual(content_json["document"], SAMPLE_DATA_1["hash"])
