# Generated by Django 4.2.2 on 2023-06-15 10:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QR',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('agent_id', models.UUIDField(editable=False)),
                ('product_id', models.UUIDField(editable=False)),
                ('generated_date', models.CharField(max_length=200)),
                ('amount', models.CharField(max_length=200)),
                ('tag', models.CharField(max_length=200)),
            ],
        ),
    ]