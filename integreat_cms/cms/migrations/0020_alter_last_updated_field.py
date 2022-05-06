# Generated by Django 3.2.13 on 2022-05-04 12:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    """
    Alter field last_updated of AbstractContentTranslation model
    """

    dependencies = [
        ("cms", "0019_add_location_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventtranslation",
            name="last_updated",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="modification date"
            ),
        ),
        migrations.AlterField(
            model_name="imprintpagetranslation",
            name="last_updated",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="modification date"
            ),
        ),
        migrations.AlterField(
            model_name="pagetranslation",
            name="last_updated",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="modification date"
            ),
        ),
        migrations.AlterField(
            model_name="poitranslation",
            name="last_updated",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="modification date"
            ),
        ),
    ]
