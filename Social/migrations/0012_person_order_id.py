# Generated by Django 5.0.7 on 2024-10-13 06:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Social", "0011_remove_person_pickup_address_alter_person_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="Order_Id",
            field=models.CharField(default="DEFAULT_ORDER_ID", max_length=16),
            preserve_default=False,
        ),
    ]
