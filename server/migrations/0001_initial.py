# Generated by Django 4.0.3 on 2022-04-02 18:44

import Server.models
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('is_seller', models.BooleanField()),
                ('wallet_hash', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=60)),
                ('seat', models.CharField(max_length=60)),
                ('price', models.IntegerField()),
                ('sale', models.BooleanField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Server.user')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_restriction', models.BooleanField()),
                ('images', djongo.models.fields.ArrayField(default=list, model_container=Server.models.URL)),
                ('tickets_remaining', models.IntegerField()),
                ('vendor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Server.user')),
            ],
        ),
    ]
