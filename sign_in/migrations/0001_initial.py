# Generated by Django 2.2.6 on 2019-11-17 06:11

from django.db import migrations, models
import sign_in.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=30)),
                ('number', models.CharField(blank=True, max_length=30, null=True)),
                ('name', models.CharField(blank=True, max_length=16, null=True)),
                ('surname', models.CharField(blank=True, max_length=16, null=True)),
                ('balance', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateField(blank=True, max_length=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoginValue',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('sys_id', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=127, unique=True)),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('iin', models.CharField(max_length=12, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'user_data',
            },
            managers=[
                ('objects', sign_in.models.MyUserManager()),
            ],
        ),
    ]
