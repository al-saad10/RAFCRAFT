# Generated by Django 5.0.3 on 2024-04-16 14:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0003_alter_cart_options_remove_cart_product_and_more"),
        ("products", "0006_product_material_product_warranty_policy_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cart",
            options={},
        ),
        migrations.RemoveField(
            model_name="cart",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="cart",
            name="session_id",
        ),
        migrations.RemoveField(
            model_name="cart",
            name="updated_at",
        ),
        migrations.AddField(
            model_name="cart",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="products.product",
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterModelTable(
            name="cart",
            table=None,
        ),
        migrations.DeleteModel(
            name="CartItem",
        ),
    ]