# Generated by Django 5.0.7 on 2024-11-11 19:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Social", "0031_person_current_location_shipmentstep"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="Shipmentsteps",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name="ShipmentStep",
        ),
    ]
