# Generated by Django 3.2.9 on 2021-12-22 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_registration_advertisements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='advertisements',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.advertisement'),
        ),
    ]
