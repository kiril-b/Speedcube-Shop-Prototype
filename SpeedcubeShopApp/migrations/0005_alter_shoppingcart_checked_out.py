# Generated by Django 4.2.2 on 2023-06-29 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SpeedcubeShopApp', '0004_category_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='checked_out',
            field=models.BooleanField(default=False, null=True),
        ),
    ]