# Generated by Django 5.1.6 on 2025-02-18 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_order_reference_id_alter_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='printed',
        ),
    ]
