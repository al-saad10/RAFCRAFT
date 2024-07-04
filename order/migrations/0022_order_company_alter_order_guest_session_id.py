# Generated by Django 5.0.3 on 2024-05-04 16:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0021_remove_order_state_alter_order_guest_session_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="company",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="guest_session_id",
            field=models.CharField(
                blank=True,
                default="94da09c1205d4e5b912496948189b560",
                max_length=255,
                null=True,
            ),
        ),
    ]
