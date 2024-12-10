# Generated by Django 5.1.2 on 2024-12-09 04:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("voter_analytics", "0004_alter_voter_zip_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="voter_score",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="voter",
            name="zip_code",
            field=models.CharField(default="00000", max_length=10),
        ),
    ]