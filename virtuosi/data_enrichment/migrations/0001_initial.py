# Generated by Django 3.1 on 2020-12-07 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_order', models.FloatField()),
                ('purchase_order_line', models.FloatField()),
                ('supplier_name', models.CharField(max_length=256)),
                ('spend', models.FloatField()),
                ('document_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_enrichment.document')),
            ],
        ),
    ]