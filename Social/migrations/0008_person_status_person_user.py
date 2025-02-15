# Generated by Django 5.0.7 on 2024-09-27 20:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Social", "0007_person_delete_shipmentbooking"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="status",
            field=models.CharField(
                choices=[("pending", "Pending"), ("completed", "Completed")],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
