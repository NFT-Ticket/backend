# Generated by Django 4.0.3 on 2022-04-04 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_restriction', models.BooleanField()),
                ('tickets_remaining', models.IntegerField()),
                ('name', models.CharField(default='', max_length=60)),
                ('description', models.CharField(default='', max_length=256)),
                ('location_name', models.CharField(default='', max_length=60)),
                ('address', models.CharField(default='', max_length=60)),
                ('city', models.CharField(default='', max_length=30)),
                ('state', models.CharField(default='', max_length=30)),
                ('date', models.DateField(default='2000-01-01')),
                ('time', models.TimeField(default='00:00:00')),
            ],
        ),
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
                ('event', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='server.event')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.user')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.user'),
        ),
    ]
