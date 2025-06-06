# Generated by Django 5.0.7 on 2024-11-11 10:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Social", "0029_alter_receipt_payment_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipt",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("unpaid", "Unpaid"),
                    ("paid", "Paid"),
                    ("refunded", "Refunded"),
                ],
                default="unpaid",
                max_length=10,
            ),
        ),
    ]
