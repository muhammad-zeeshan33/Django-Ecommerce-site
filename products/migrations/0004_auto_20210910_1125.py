# Generated by Django 3.2.7 on 2021-09-10 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='size',
            new_name='size_1',
        ),
        migrations.AddField(
            model_name='product',
            name='size_2',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='product',
            name='size_3',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
