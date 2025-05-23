# Generated by Django 5.0.7 on 2024-09-28 18:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Social", "0010_rename_date_person_date_created_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="person",
            name="pickup_address",
        ),
        migrations.AlterField(
            model_name="person",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("completed", "Completed"),
                    ("Transit", "Transit"),
                    ("processing", "processing"),
                    ("Cleared", "Cleared"),
                    ("Detained", "Detained"),
                    ("Despatched", "Despatched"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
