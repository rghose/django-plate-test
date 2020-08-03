from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.utils import timezone

from .view.invoice import Invoice
from client.models import InvoiceDocument

class MockFile():
    def __init__(self, data):
        self.data = data
    def read(self):
        return self.data.encode()

class InvoiceDocumentTest(TestCase):
    def test_get_sha1(self):
        result = Invoice.process_in_memory_file(MockFile("mockdata"))
        self.assertEqual(result, "8bc86513cfd731529471437f987663669d915cf5")
    
    def test_multiple_uploads_dont_create_duplicates(self):
        result1 = Invoice.process_in_memory_file(MockFile("mockdata"))
        result2 = Invoice.process_in_memory_file(MockFile("mockdata"))
        self.assertEqual(result1, result2)
        q = InvoiceDocument.objects.all()
        self.assertEqual(len(q), 1)
