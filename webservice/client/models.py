from django.db import models

# Create your models here.
class InvoiceDocument(models.Model):
    # store the document in the model, upto a max size of 1 MB.
    document_content = models.BinaryField(max_length=100000)
    document_sha1 = models.CharField(max_length=40, primary_key=True)
    status = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField('date created')
    def __str__(self):
        return "%s \"%s\"" % (self.document_sha1, self.created_at)

class DigitizedInvoice(models.Model):
    document_sha1 = models.ForeignKey(InvoiceDocument, on_delete=models.CASCADE)
    data_json = models.CharField(max_length=500)
    created_at = models.DateTimeField('date when status was changed')
    def __str__(self):
        return "%s \"%s\"" % (self.document_sha1, self.created_at)
