# Generated by Django 5.2 on 2025-04-17 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "task_manager",
            "0004_status_created_at_alter_label_name_alter_status_name_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="status",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Date Created"
            ),
        ),
    ]
