# Generated by Django 5.0.7 on 2024-08-15 17:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Social", "0002_shipmentbooking"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shipmentbooking",
            name="contact_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
