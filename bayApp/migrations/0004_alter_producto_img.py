# Generated by Django 4.1.2 on 2023-06-04 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bayApp', '0003_alter_producto_totalproducto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='img',
            field=models.CharField(max_length=200),
        ),
    ]