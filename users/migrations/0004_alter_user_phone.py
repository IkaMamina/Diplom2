# Generated by Django 5.1.4 on 2024-12-08 17:20

import users.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_ref_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                help_text="Введите номер телефона",
                max_length=11,
                unique=True,
                validators=[users.validators.phone_validator],
                verbose_name="Телефон",
            ),
        ),
    ]