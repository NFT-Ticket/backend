# Generated by Django 3.2.12 on 2022-04-03 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Server', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='vendor_id',
            new_name='vendor',
        ),
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='event',
            name='location_name',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AddField(
            model_name='event',
            name='state',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.TimeField(default='00:00:00'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Server.event'),
        ),
    ]