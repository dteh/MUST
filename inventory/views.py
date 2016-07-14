from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.db.models import Q
from .models import Gender,Size,Category,Item,Customer,Brand, Order
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

#### TODO:
#
# 1. Implement order searching for returns - done
# 2. Convert all old 'add' pages to use new header - done
# 3. Figure out how to host this..
#
#### MAYBE:
# 1. Implement per order discounting
# 2. Implement item level returns (partial order returns)
# 3. Implement Overdue EMAILS
# 4. Better inventory searching (stocktake purposes)
# 5. $$ tallies


def home(request):
	return render(request,'inventory/home.html')

def add(request):
	return render(request,'inventory/add.html')

def add_item(request):
	if request.method == 'GET':
		genders = Gender.objects.all()
		sizes = Size.objects.all()
		categories = Category.objects.all()
		context = {'genders':genders,'categories':categories,'sizes':sizes}
	elif request.method == 'POST':
		item = Item(item_name=request.POST['item_name'],category_id=request.POST['category'],\
			size_id=request.POST['size'],gender_id=request.POST['gender'])
		item.save()
		genders = Gender.objects.all()
		sizes = Size.objects.all()
		categories = Category.objects.all()
		context = {'new_addition':request.POST['item_name'],'genders':genders,'categories':categories,'sizes':sizes}
	return render(request,'inventory/addItem.html',context)

def add_category(request):
	if request.method == 'POST':
		category = Category(category_name=request.POST['category_name'],cost_per_day=request.POST['cost_per_day'])
		category.save()
		context = {'new_addition':request.POST['category_name']}
		return render(request,'inventory/addCategory.html',context)
	return render(request,'inventory/addCategory.html')

def add_size(request):
	if request.method == 'POST':
		size = Size(size_name = request.POST['size_name'])
		size.save()
		context = {'new_addition':request.POST['size_name']}
		return render(request,'inventory/addSize.html',context)		
	return render(request,'inventory/addSize.html')

def add_gender(request):
	if request.method == 'POST':
		gender = Gender(gender_name = request.POST['gender_name'])
		gender.save()
		context = {'new_addition':request.POST['gender_name']}
		return render(request,'inventory/addGender.html',context)
	return render(request,'inventory/addGender.html')

def add_customer(request):
	if request.method == 'POST':
		customer = Customer(first_name=request.POST['first_name'],last_name=request.POST['last_name'],\
			email=request.POST['email'],phone=request.POST['phone'],is_uom_student=request.POST.get('is_uom_student',False))
		customer.save()
		context = {'new_addition':request.POST['first_name']+" "+request.POST['last_name']}
		return render(request,'inventory/addCustomer.html',context)		
	return render(request,'inventory/addCustomer.html')

def add_brand(request):
	if request.method == "POST":
		brand = Brand(brand_name=request.POST['brand_name'])
		brand.save()
		context = {'new_addition':request.POST['brand_name']}
		return render(request,'inventory/addBrand.html',context)
	return render(request,'inventory/addBrand.html')


################

def add_order(request):
	return render(request,'inventory/addOrder.html')

def add_order_customer(request,customer_id):
	x = Customer.objects.filter(customer_id=customer_id)
	context = {'fname':x[0].first_name,'lname':x[0].last_name, 'cid':customer_id}	
	return render(request,'inventory/addOrderCustomer.html',context)

def add_order_duration(request,customer_id):
	if request.method == "POST":
		x = Customer.objects.filter(customer_id=customer_id)
		items = request.POST.getlist('item')
		returnItems = Item.objects.filter(item_id__in=items)
		cpd=0
		for i in returnItems:
			cpd += i.category.cost_per_day
		context = {'fname':x[0].first_name,'lname':x[0].last_name, 'cid':customer_id,'itemids':items,'data':returnItems, 'cpd':cpd}

	return render(request,"inventory/addOrderDuration.html",context)

@transaction.atomic
def add_order_finalise(request,customer_id):
	if request.method == "POST":
		discount = 0
		x = Customer.objects.filter(customer_id=customer_id)
		cpd = request.POST['cpd']
		days = request.POST['days']
		returnDate = request.POST['returndate']
		items = request.POST.getlist('item')
		returnItems = Item.objects.filter(item_id__in=items)
		creator = request.user.id
		
		order = Order(cpd=cpd,order_length=days,order_due=returnDate,createdby_id=creator,customer_id=customer_id)
		order.save()
		order.order_items.add(*items)
		order.save()

		for item in returnItems:
			item.available = not item.available
			item.save()

		context = {'complete':False,'fname':x[0].first_name,'lname':x[0].last_name,'data':returnItems,'total':int(cpd)*int(days)-int(discount),\
		'cpd':cpd,'days':days,'returndate':returnDate,'oid':order.order_id,'paid':order.paid, 'discount':discount, 'status':order.get_status_display()}

		return render(request,'inventory/addOrderSummary.html',context)

def get_available_inventory(request):
	if request.is_ajax():
		available = Item.objects.filter(available=True)
		allowed_filters = ['category','gender','size','brand']
		kwarg = {}
		for fil in allowed_filters:
			if request.GET.get(fil):
				kwarg[fil] = request.GET[fil]
		available = available.filter(**kwarg)
		if available.count()==0:
			data = '[{No results found for selected filters}]'
		else:
			data = serializers.serialize('json',available)
		return HttpResponse(data,'json')

def get_categories(request):
	if request.is_ajax():
		cats = Category.objects.all()
		data = serializers.serialize('json',cats)
		return HttpResponse(data,'json') 

def get_sizes(request):
	if request.is_ajax():
		sz = Size.objects.all()
		data = serializers.serialize('json',sz)
		return HttpResponse(data,'json') 

def get_genders(request):
	if request.is_ajax():
		genders = Gender.objects.all()
		data = serializers.serialize('json',genders)
		return HttpResponse(data,'json') 

def get_brands(request):
	if request.is_ajax():
		brands = Brand.objects.all()
		data = serializers.serialize('json',brands)
		return HttpResponse(data,'json') 

def get_customers(request,search=None):
	if request.is_ajax():
		# print("Search term:",search)
		if search == None:
			cust = Customer.objects.all()
		else:
			cust = Customer.objects.filter(
				Q(first_name__contains=search) | Q(last_name__contains=search)
			)
		data = serializers.serialize('json',cust)
		if data == "[]":
			print('nothing found')
		return HttpResponse(data,'json') 

def view_order(request,order_id):
	if request.method == "GET":
		complete = False
		order = Order.objects.get(order_id=order_id)
		if order.status == 'c':
			complete = True

		print(order.get_status_display())
		context = {'complete':complete,'returnpage':True, 'fname':order.customer.first_name,'lname':order.customer.last_name,'data':order.order_items.all(),'total':int(order.cpd)*int(order.order_length)-int(order.discount),\
		'cpd':order.cpd,'days':order.order_length,'returndate':order.order_due,'oid':order.order_id,'paid':order.paid, 'discount':order.discount, 'status':order.get_status_display()}

		return render(request,'inventory/addOrderSummary.html',context)

def view_all_orders(request):
	if request.method == "GET":
		data = Order.objects.all()
		context = {'title':'All Orders','data':data}
		return render(request,'inventory/viewAllOrders.html',context)

def view_outstanding_orders(request):
	if request.method =="GET":
		data = Order.objects.filter(
			Q(status='a') | Q(status='x') | Q(status='o')
		)
		context = {'title':'Outstanding Orders','data':data}
		return render(request,'inventory/viewAllOrders.html',context)

def view_search_orders(request):
	if request.method == "GET":
		return render(request,'inventory/orderSearch.html')

def get_search_orders(request,search=None):
	if request.is_ajax():
		# print("Search term:",search)
		if search == None:
			order = Order.objects.filter(
				Q(status='a') | Q(status='x') | Q(status='o')
			)
		else:
			order = Order.objects.filter(
				(Q(customer__first_name__contains=search) | Q(customer__last_name__contains=search) | Q(order_items__item_name__contains=search) | Q(order_items__brand__brand_name__contains=search))& (Q(status='a') | Q(status='x') | Q(status='o'))
			)
		data = serializers.serialize('json',order, use_natural_foreign_keys=True)
		if data == "[]":
			print('nothing found')
		return HttpResponse(data,'json') 

@transaction.atomic
def change_status(request, order_id):
	if request.method == "GET":
		order = Order.objects.get(order_id=order_id)
		order.paid = not order.paid
		order.save()

		context = {'complete':False,'returnpage':True, 'fname':order.customer.first_name,'lname':order.customer.last_name,'data':order.order_items.all(),'total':int(order.cpd)*int(order.order_length)-int(order.discount),\
		'cpd':order.cpd,'days':order.order_length,'returndate':order.order_due,'oid':order.order_id,'paid':order.paid, 'discount':order.discount, 'status':order.get_status_display()}

		return render(request,'inventory/addOrderSummary.html',context)

@transaction.atomic
def return_order(request, order_id):
	if request.method == "GET":
		order = Order.objects.get(order_id=order_id)
		order.status = 'c'
		order.save()

		for item in order.order_items.all():
			print(item.item_name)
			print(item.available)
			item.available = not item.available
			print('changed to',item.available)
			item.save()

		context = {'complete':True,'fname':order.customer.first_name,'lname':order.customer.last_name,'data':order.order_items.all(),'total':int(order.cpd)*int(order.order_length)-int(order.discount),\
		'cpd':order.cpd,'days':order.order_length,'returndate':order.order_due,'oid':order.order_id,'paid':order.paid, 'discount':order.discount, 'status':order.get_status_display()}

		return render(request,'inventory/addOrderSummary.html',context)

def view_all(request):
	customers = [i for i in Customer.objects.all()]
	items = [i for i in Item.objects.all()]
	genders = [i.gender_name for i in Gender.objects.all()]
	sizes = [i.size_name for i in Size.objects.all()]
	categories = [i.category_name for i in Category.objects.all()]
	context = {'customers':customers,'items':items,'genders':genders,'sizes':sizes,'categories':categories}
	return render(request,'inventory/viewAll.html',context)
