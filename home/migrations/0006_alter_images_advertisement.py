# Generated by Django 3.2.10 on 2021-12-28 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_profile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='advertisement',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='home.advertisement'),
        ),
    ]
