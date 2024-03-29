# Generated by Django 3.2.23 on 2024-02-18 20:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0007_alter_product_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=30, null=True)),
                ('percent', models.PositiveIntegerField(default=0, null=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date_time', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=300)),
                ('phone_number', models.CharField(max_length=19)),
                ('address_line1', models.CharField(max_length=70)),
                ('address_line2', models.CharField(max_length=70)),
                ('address_line3', models.CharField(blank=True, max_length=70, null=True)),
                ('region', models.CharField(max_length=85)),
                ('city', models.CharField(max_length=85)),
                ('postcode', models.CharField(blank=True, max_length=30, null=True)),
                ('country', models.CharField(max_length=56)),
                ('order_number', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('order_status', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='OrderLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('product_quantity', models.IntegerField(default=1)),
                ('order_subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('discount', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='discount', to='checkout.discount')),
                ('order_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='checkout.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
