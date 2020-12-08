import os
import xlrd

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import Http404, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files.storage import default_storage

from .models import Document, Lines
from .forms import DocumentForm


class IndexView(View):
    def get(self, request):
        """Return the home page."""

        response = render(request, "data_enrichment/index.html", {})
        return response


class ListView(View):
    def get(self, request):
        """Return the document list view page."""
        records = Document.objects.all()
        uploaded_files = []
        for record in records:
            uploaded_files.append(
                {
                    "file_name": str(record.document).split("/")[1],
                    "uploaded_at": record.uploaded_at,
                }
            )
        response = render(
            request,
            "data_enrichment/list_view.html",
            {
                "uploaded_files": records,
            },
        )
        return response


class UploadDocumentView(View):
    def get(self, request):
        """Return the document upload page."""
        form = DocumentForm(request.POST, request.FILES)
        response = render(
            request, "data_enrichment/upload.html", {"form": form}
        )
        return response

    def post(self, request):
        """ """
        form = DocumentForm(request.POST, request.FILES)
        MEDIA_PATH = settings.MEDIA_ROOT
        print(form, "=========form")
        if form.is_valid():
            record = form.save()
            filename = str(record.document)
            if not (filename.endswith(".xlsx") or filename.endswith(".xls")):
                return render(
                    request, "data_enrichment/upload.html", {"form": form}
                )
            excel_data = xlrd.open_workbook(
                os.path.join(MEDIA_PATH, str(record.document))
            )
            sheet = excel_data.sheet_by_index(0)
            keys = ["purchase_order", "purchase_order_line", "supplier_name", "spend"]
            dict_list = []
            for row_index in range(1, sheet.nrows):
                d = {
                    keys[col_index]: sheet.cell(row_index, col_index).value
                    for col_index in range(sheet.ncols)
                }
                d["document_id"] = record
                dict_list.append(d)
            obj_list = [Lines(**data_dict) for data_dict in dict_list]
            Lines.objects.bulk_create(obj_list)
            return redirect("list")
        else:
            form = DocumentForm()
        return render(request, "data_enrichment/upload.html", {"form": form})


class DeleteView(View):
    def post(self, request, pk):
        """Return the document delete view page."""
        record = get_object_or_404(Document, pk=pk)
        record.delete()
        return redirect('list')


class RulesView(View):

    def get(self, request):
        return

    def post(self, request):
        return
