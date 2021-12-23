# Generated by Django 3.2.9 on 2021-12-22 22:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('house_type', models.CharField(choices=[('green', 'GREEN'), ('blue', 'BLUE'), ('red', 'RED'), ('orange', 'ORANGE'), ('black', 'BLACK')], default='green', max_length=6)),
                ('house_address', models.TextField(max_length=255)),
                ('rent_fee', models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(5000), django.core.validators.MaxValueValidator(100000)])),
                ('image', models.ImageField(upload_to='images/')),
            ],
            options={
                'verbose_name': 'Advertisement',
                'verbose_name_plural': 'Advertisements',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('mobile', models.IntegerField(unique=True)),
                ('address', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('advertisements', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='home.advertisement')),
            ],
            options={
                'verbose_name': 'Registration',
                'verbose_name_plural': 'Registrations',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.FileField(upload_to='images/')),
                ('advertisement', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='home.advertisement')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.AddField(
            model_name='advertisement',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.registration'),
        ),
    ]
