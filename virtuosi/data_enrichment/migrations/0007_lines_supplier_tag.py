# Generated by Django 3.1 on 2020-12-11 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_enrichment', '0006_generictags'),
    ]

    operations = [
        migrations.AddField(
            model_name='lines',
            name='supplier_tag',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]