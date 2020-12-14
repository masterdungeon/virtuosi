import os
import xlrd
import xlwt
import zipfile
from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import Http404, HttpResponse
from django.conf import settings
from django.db.models import Count, Sum
from django.forms.models import inlineformset_factory

from .models import Document, Lines, Rules, RuleCondition, RuleRunTrack
from .models import GenericTags
from .forms import DocumentForm, RulesView, RuleConditionForm


class IndexView(View):

    def get(self, request):
        """Return the home page."""
        return redirect("list")


class ListView(View):

    def get(self, request):
        """Return the document list view page."""

        records = Document.objects.all()
        uploaded_files = []
        for record in records:
            uploaded_files.append(
                {
                    "id": record.id,
                    "file_name": str(record.document).split("/")[1],
                    "uploaded_at": record.uploaded_at,
                }
            )
        response = render(
            request,
            "data_enrichment/list_view.html",
            {
                "uploaded_files": uploaded_files,
            },
        )
        return response


class UploadDocumentView(View):

    def get(self, request):
        """Return the document upload page."""

        form = DocumentForm(request.POST, request.FILES)
        response = render(request, "data_enrichment/upload.html", {"form": form})
        return response

    def post(self, request):
        """Return upload page with saving current upaloaded file in document."""

        form = DocumentForm(request.POST, request.FILES)
        MEDIA_PATH = settings.MEDIA_ROOT
        if form.is_valid():
            record = form.save()
            filename = str(record.document)
            if not (filename.endswith(".xlsx") or filename.endswith(".xls")):
                return render(request, "data_enrichment/upload.html", {"form": form})
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
        return redirect("list")


# class RulesView(View):

#     def get(self, request):
#         """Return the view of Rules and Rule Conditions."""

#         data = []
#         for rule in Rules.objects.all():
#             conditions = RuleCondition.objects.filter(rule_id=rule.id)
#             data.append(
#                 {
#                     "rule_id": rule.id,
#                     "rule_name": rule.rule_name,
#                     "rule_desc": rule.rule_desc,
#                     "rule_conditions": conditions,
#                 }
#             )
#         response = render(request, "data_enrichment/rule.html", {"rules": Rules.objects.all()})
#         return response


# class RuleRunView(View):

def rule_run(request, pk):
    """Return rules page with applying current rule and tag on all documents."""

    rule = Rules.objects.filter(id=pk).first()
    conditions = RuleCondition.objects.filter(rule_id=pk)
    column_name = rule.rule_name
    documents = Document.objects.all()
    for document in documents:
        data = []
        groupby = (
            Lines.objects.filter(document_id=document.id)
            .values("supplier_name")
            .annotate(total_price=Sum("spend"))
        )
        for idx, item in enumerate(groupby):
            query = (
                "select * from data_enrichment_generictags where %s >= value_from and %s <= value_to;"
                % (item["total_price"], item["total_price"])
            )
            tags = GenericTags.objects.raw(
                query,
            )
            for tag in tags:
                item["tag"] = tag.tag
                data.append(
                    {
                        "tag": tag.tag,
                        "supplier_name": item["supplier_name"],
                        "total_price": item["total_price"],
                    }
                )
        if not data:
            lines = Lines.objects.filter(
                document_id=document.id,
            )
            lines.update(supplier_tag='')
        for item in data:
            lines = Lines.objects.filter(
                document_id=document.id,
                supplier_name__contains=item["supplier_name"],
            )
            lines.update(supplier_tag=item["tag"])
    RuleRunTrack.objects.create(rule_id=rule, column_name=column_name)
    for condition in conditions:
        group_name = str(condition.value_from) + "-" + str(condition.value_to)
        lines = Lines.objects.filter(
            spend__range=(condition.value_from, condition.value_to)
        )
        lines.update(group_name=group_name)
    return redirect("rules")


class TemplateView(View):

    def get(self, request):
        """Return the direct download of uploading file excel format."""

        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="format.xlsx"'
        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Upload data")
        row_num = 0
        font_style = xlwt.XFStyle()
        columns = ["Purchase Order", "Purchase Order Line", "Supplier Name", "Spend"]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        wb.save(response)
        return response


class DownloadView(View):

    def get(self, request):
        """Return the direct download of zip file that contains all output excel file."""

        try:
            track = RuleRunTrack.objects.latest("id")
        except RuleRunTrack.DoesNotExist:
            ## Either Rule not created or nor runned any one.
            ## Crrate or run Rule.
            return redirect("rules")
        records = Document.objects.all()
        zip_subdir = "output_" + track.rule_id.rule_name
        zip_filename = "%s.zip" % zip_subdir
        s = BytesIO()
        zf = zipfile.ZipFile(s, "w")
        tags_count = len(GenericTags.objects.all())
        for record in records:
            filename = str(record.document).split("/")[1].split(".")[0]
            filename = filename + "_" + track.rule_id.rule_name
            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("Purchase Value Grouping")
            row_num = 0
            font_style = xlwt.XFStyle()
            columns = [
                "Purchase Order",
                "Purchase Order Line",
                "Supplier Name",
                "Spend",
                track.column_name,
            ]
            if tags_count:
                columns.append("Supplier Tag")
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            lines = Lines.objects.filter(document_id=record.id).order_by("id")
            for idx, line in enumerate(lines):
                ws.write(idx + 1, 0, line.purchase_order, font_style)
                ws.write(idx + 1, 1, line.purchase_order_line, font_style)
                ws.write(idx + 1, 2, line.supplier_name, font_style)
                ws.write(idx + 1, 3, line.spend, font_style)
                ws.write(idx + 1, 4, line.group_name, font_style)
                if tags_count:
                    ws.write(idx + 1, 5, line.supplier_tag, font_style)
            file_name = filename + ".xlsx"
            wb.save(file_name)
            zip_path = os.path.join(zip_subdir, file_name)
            zf.write(file_name, zip_path)
            os.unlink(file_name)
        zf.close()
        resp = HttpResponse(s.getvalue(), content_type="application/zip")
        resp["Content-Disposition"] = "attachment; filename=%s" % zip_filename
        return resp


def rules(request):
    response = render(request, "data_enrichment/rule.html", {"rules": Rules.objects.all()})
    return response

def rule_create(request, template_name='data_enrichment/rule_form.html'):
    InlineFormSet = inlineformset_factory(Rules, RuleCondition, form=RuleConditionForm, extra=6)
    form = RulesView(request.POST or None)
    formset = InlineFormSet(request.POST or None, instance=Rules())
    if form.is_valid() and formset.is_valid():
        rule = form.save()
        formset.instance = rule
        formset.save()
        return redirect('rules')
    ctx = {
        'form': form,
        'formset': formset,
    }
    return render(request, template_name, ctx)

def rule_update(request, pk, template_name='data_enrichment/rule_form.html'):
    InlineFormSet = inlineformset_factory(Rules, RuleCondition, form=RuleConditionForm)
    rule = get_object_or_404(Rules, pk=pk)
    form = RulesView(request.POST or None, instance=rule)
    formset = InlineFormSet(request.POST or None, instance=rule)
    if form.is_valid() and formset.is_valid():
        rule = form.save()
        formset.instance = rule
        formset.save()
        return redirect('rules')
    ctx = {
        'form': form,
        'formset': formset,
    }
    return render(request, template_name, ctx)

def rule_delete(request, pk, template_name='data_enrichment/rule_confirm_delete.html'):
    rule = get_object_or_404(Rules, pk=pk)
    if request.method=='GET':
        rule.delete()
        return redirect('rules')
    ctx = {
        'rule': rule,
    }
    return render(request, template_name, ctx)
