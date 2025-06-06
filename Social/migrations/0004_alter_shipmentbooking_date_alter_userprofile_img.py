# Generated by Django 5.0.7 on 2024-08-15 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Social", "0003_alter_shipmentbooking_contact_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shipmentbooking",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="img",
            field=models.ImageField(blank=True, default="avatar.jpg", upload_to="pics"),
        ),
    ]
