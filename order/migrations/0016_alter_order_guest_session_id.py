# Generated by Django 5.0.3 on 2024-05-04 07:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0015_alter_order_guest_session_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="guest_session_id",
            field=models.CharField(
                blank=True,
                default="81165a814930436c8bcdcf9c616a510f",
                max_length=255,
                null=True,
            ),
        ),
    ]
