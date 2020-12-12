import xlwt

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Count

from .models import Document, Rules, RuleCondition, GenericTags


class SimpleTest(TestCase):

    def generate_file(self):
        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Upload data")
        row_num = 0
        font_style = xlwt.XFStyle()
        columns = ["Purchase Order", "Purchase Order Line", "Supplier Name", "Spend"]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        wb.save('test.xlsx')

    def test_index(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_list(self):
        resp = self.client.get("/list/")
        self.assertEqual(resp.status_code, 200)

    def test_upload(self):
        resp = self.client.get("/upload/")
        self.assertEqual(resp.status_code, 200)

    def test_rules(self):
        resp = self.client.get("/rules/")
        self.assertEqual(resp.status_code, 200)

    def test_template(self):
        resp = self.client.get("/template/")
        self.assertEqual(resp.status_code, 200)

    def test_document(self):
        self.generate_file()
        uploaded_file = SimpleUploadedFile('test.xlsx', content='')
        self.document = Document.objects.create(document=uploaded_file)
        count = len(Document.objects.all())
        self.assertEqual(count, 1, "Record Created.")

    def test_generic_tags(self):
        self.generic_tag_1 = GenericTags.objects.create(
            tag="Partner Supplier", value_from=1000001, value_to=100000000
        )
        self.assertEqual(self.generic_tag_1.tag, "Partner Supplier", "Generic Tag Created.")
