# Generated by Django 4.2.2 on 2023-06-28 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SpeedcubeShopApp', '0002_lubeservice_shoppingcart_onpromotion_itemorder_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_url',
            field=models.URLField(null=True),
        ),
    ]
