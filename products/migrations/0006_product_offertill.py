# Generated by Django 3.2.7 on 2021-09-11 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offertill',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
