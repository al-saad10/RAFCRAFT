# Generated by Django 5.0.3 on 2024-05-04 09:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_remove_customuserprofile_last_login_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuserprofile",
            name="date_of_birth",
        ),
    ]
