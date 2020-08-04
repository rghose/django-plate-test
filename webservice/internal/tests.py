from django.test import TestCase

from .view.invoice_manager import InvoiceManager
from client.view.invoice import InvoiceConstants

import json

SAMPLE_DATA_1 = {
    "data": "mockdata",
    "hash": "8bc86513cfd731529471437f987663669d915cf5"
}

# Create your tests here.
class InvoiceManagerTest(TestCase):
    def test_invalid_param_format(self):
        self.assertRaises(ValueError, InvoiceManager.params_from_body, "")
        self.assertRaises(ValueError, InvoiceManager.params_from_body, "id=something")
        self.assertRaises(ValueError, InvoiceManager.params_from_body, "id=something&data={}")

    def test_invalid_params(self):
        obj = dict()
        self.assertRaises(Exception, InvoiceManager.params_from_body, json.dumps(obj))
        obj = { "id": SAMPLE_DATA_1["data"] }
        self.assertRaises(Exception, InvoiceManager.params_from_body, json.dumps(obj))
        obj = { "data": "{}" }
        self.assertRaises(Exception, InvoiceManager.params_from_body, json.dumps(obj))

    def test_valid_params(self):
        obj = {"id": SAMPLE_DATA_1["data"], "data": {"invoice": "TEST123"}}
        sha1,data,status = InvoiceManager.params_from_body(json.dumps(obj))
        self.assertEquals(sha1, SAMPLE_DATA_1["data"])
        self.assertEquals(data, obj["data"])
        self.assertEquals(status, InvoiceConstants.STATUS_IN_PROGRESS)
