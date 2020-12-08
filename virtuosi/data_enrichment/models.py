from django.db import models


class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Lines(models.Model):
	document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
	purchase_order = models.FloatField()
	purchase_order_line = models.FloatField()
	supplier_name = models.CharField(max_length=256)
	spend = models.FloatField()


class Rules(models.Model):
    rule_name = models.CharField(max_length=256)
    rule_desc = models.TextField()
