from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATUSES = (
	('a','ON LOAN'),
	('o','OVERDUE'),
	('c','COMPLETED'),
	('x','LOSS')
)

class CustomerManager(models.Manager):
	def get_by_natural_key(self,first_name,last_name):
		return self.get(first_name=first_name,last_name=last_name)

class ItemManager(models.Manager):
	def get_by_natural_key(self,items):
		return self.get(items=items)

class Category(models.Model):
	category_id = models.AutoField(primary_key = True)
	category_name = models.CharField(max_length = 20)
	cost_per_day = models.DecimalField(max_digits = 5, decimal_places = 2)

class Brand(models.Model):
	brand_id = models.AutoField(primary_key = True)
	brand_name = models.CharField(max_length = 30)

class Size(models.Model):
	size_id = models.AutoField(primary_key = True)
	size_name = models.CharField(max_length = 10)

class Gender(models.Model):
	gender_id = models.AutoField(primary_key = True)
	gender_name = models.CharField(max_length = 10)

class Customer(models.Model):
	customer_id = models.AutoField(primary_key = True)
	first_name = models.CharField(max_length = 20)
	last_name = models.CharField(max_length = 20)
	phone = models.CharField(max_length = 13)
	is_uom_student = models.BooleanField(default = True)
	email = models.EmailField()

	objects = CustomerManager()
	def natural_key(self):
		return (self.first_name,self.last_name)

class Item(models.Model):
	item_id = models.AutoField(primary_key = True)
	item_name = models.CharField(max_length = 50)
	category = models.ForeignKey(Category, on_delete = models.PROTECT)
	size = models.ForeignKey(Size, on_delete = models.PROTECT)
	gender = models.ForeignKey(Gender, on_delete = models.PROTECT)
	brand = models.ForeignKey(Brand, on_delete = models.PROTECT)
	available = models.BooleanField(default = True)

	objects = ItemManager()
	def natural_key(self):
		return (self.item_name,self.brand.brand_name)
	natural_key.dependencies = ['inventory.brand']

class Order(models.Model):
	order_id = models.AutoField(primary_key = True)
	order_items = models.ManyToManyField(Item)
	order_date = models.DateField(auto_now_add = True)
	order_length = models.IntegerField()
	order_due = models.DateField()
	createdby = models.ForeignKey(User, on_delete = models.PROTECT)
	customer = models.ForeignKey(Customer, on_delete = models.PROTECT)
	cpd = models.IntegerField()
	discount = models.DecimalField(max_digits = 5, decimal_places = 2, default=0.00)
	paid = models.BooleanField(default = False)
	status = models.CharField(max_length=1,choices=STATUSES,default='a')