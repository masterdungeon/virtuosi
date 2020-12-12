from django.db import models


class Document(models.Model):
    """Model used to store excel file."""

    document = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Lines(models.Model):
    """Model used to store excel file rows."""

    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    purchase_order = models.FloatField()
    purchase_order_line = models.FloatField()
    supplier_name = models.CharField(max_length=256)
    spend = models.FloatField()
    group_name = models.CharField(max_length=256)
    supplier_tag = models.CharField(max_length=256)


class Rules(models.Model):
    """Model used to store Rules."""

    rule_name = models.CharField(max_length=256)
    rule_desc = models.TextField()

    def __str__(self):
        return self.rule_name


class RuleCondition(models.Model):
    """Model used to store Rule Conditios."""

    rule_id = models.ForeignKey(Rules, on_delete=models.CASCADE)
    field = models.CharField(max_length=256)
    value_from = models.IntegerField()
    value_to = models.IntegerField()
    tag = models.CharField(max_length=256)


class RuleRunTrack(models.Model):
    """Model used to track record of rule running."""

    rule_id = models.ForeignKey(Rules, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=256)


class GenericTags(models.Model):
    """Model used to store Genric Tags."""

    tag = models.CharField(max_length=256)
    value_from = models.IntegerField()
    value_to = models.IntegerField()

    def __str__(self):
        return self.tag
