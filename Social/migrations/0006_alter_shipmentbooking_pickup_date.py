# Generated by Django 5.0.7 on 2024-09-15 05:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Social", "0005_remove_userprofile_img_shipmentbooking_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shipmentbooking",
            name="pickup_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
