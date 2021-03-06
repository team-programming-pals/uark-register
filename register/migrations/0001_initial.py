# Generated by Django 3.1 on 2020-09-22 22:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveUser',
            fields=[
                ('activeUUID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('activeEmployeeUUID', models.UUIDField(db_index=True)),
                ('activeName', models.CharField(default='', max_length=256)),
                ('activeClassification', models.IntegerField(default=0)),
                ('activeSessionKey', models.CharField(db_index=True, default='', max_length=128)),
                ('activeCreationDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employeeUUID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('employeeID', models.IntegerField(db_index=True, default=0)),
                ('employeeFirstName', models.CharField(default='', max_length=128)),
                ('employeeLastName', models.CharField(default='', max_length=128)),
                ('employeePassword', models.CharField(default='', max_length=128)),
                ('employeeActive', models.BooleanField(default=False)),
                ('employeeClassification', models.IntegerField(default=0)),
                ('employeeeManagerUUID', models.UUIDField(default='00000000-0000-0000-0000-000000000000', editable=False)),
                ('employeeCreationDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productUUID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('productCode', models.CharField(db_index=True, default='', max_length=32)),
                ('productCount', models.IntegerField(default=0)),
                ('productCreationDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
