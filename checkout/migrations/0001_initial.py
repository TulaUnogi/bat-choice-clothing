# Generated by Django 3.2.23 on 2024-04-30 21:23

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_auto_20240430_2103'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_code', models.CharField(blank=True, max_length=30, null=True)),
                ('percent', models.PositiveIntegerField(default=0, null=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date_time', models.DateTimeField(auto_now_add=True)),
                ('full_name', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(max_length=300)),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True)),
                ('address_line1', models.CharField(default='', max_length=200)),
                ('address_line2', models.CharField(default='', max_length=200)),
                ('region', models.CharField(max_length=85)),
                ('city', models.CharField(max_length=85)),
                ('postcode', models.CharField(blank=True, max_length=30, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('order_number', models.CharField(db_index=True, editable=False, max_length=32, unique=True)),
                ('order_status', models.CharField(choices=[('Awaiting Fulfillment', 'Awaiting Fulfillment'), ('Awaiting Shipment', 'Awaiting Shipment'), ('Order Shipped', 'Order Shipped'), ('Order Completed', 'Order Completed'), ('Cancelled', 'Cancelled'), ('Refunded', 'Refunded'), ('Partially Refunded', 'Partially Refunded'), ('Disputed', 'Disputed')], default='Awaiting Fulfillment', max_length=40)),
                ('order_subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('discount', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount', to='checkout.discount')),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='userprofile.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('product_quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='checkout.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
