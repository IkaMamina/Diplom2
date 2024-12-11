# Generated by Django 5.1.4 on 2024-12-08 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_invite_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="ref_code",
            field=models.CharField(
                blank=True, max_length=6, null=True, verbose_name="Введенный инвайт код"
            ),
        ),
    ]