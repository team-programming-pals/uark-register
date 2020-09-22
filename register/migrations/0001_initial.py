"""
Helpful Resources:

    1. https://docs.djangoproject.com/en/3.1/topics/migrations/
"""
from django.db import migrations, models
import uuid


# Create the Products database table
class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
