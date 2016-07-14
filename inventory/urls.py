from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.home),
    url(r'^add/$', views.add, name='add'),
    url(r'^add/gender/$', views.add_gender, name='add_gender'),
    url(r'^add/customer/$', views.add_customer, name='add_customer'),
    url(r'^add/size/$', views.add_size, name='add_size'),
    url(r'^add/category/$', views.add_category, name='add_category'),
    url(r'^add/item/$', views.add_item, name='add_item'),
    url(r'^add/brand/$',views.add_brand,name='add_brand'),
    url(r'^add/order/$',views.add_order,name='add_order'),
    url(r'^add/order/(?P<customer_id>[0-9]+)/$',views.add_order_customer,name='add_order_customer'),
    url(r'^add/order/(?P<customer_id>[0-9]+)/duration/$',views.add_order_duration,name='add_order_duration'),
    url(r'^add/order/(?P<customer_id>[0-9]+)/duration/finalise/$',views.add_order_finalise,name='add_order_summary'),
    url(r'^add/get_inventory/$',views.get_available_inventory,name='add_order_get_inventory'),
    url(r'^add/get_categories/$',views.get_categories,name='enum_categories'),
    url(r'^add/get_sizes/$',views.get_sizes,name='enum_sizes'),
    url(r'^add/get_genders/$',views.get_genders,name='enum_genders'),
    url(r'^add/get_brands/$',views.get_brands,name='enum_brands'),
    url(r'^add/order/test/$',views.add_order_customer,name='add_order_duration'),
    url(r'^add/get_customers/$',views.get_customers,name='get_customers'),
    url(r'^add/get_customers/(?P<search>.*)$',views.get_customers),

    url(r'^view/order/$',views.view_all_orders,name='view_all_orders'),
    url(r'^view/order/return/$',views.view_search_orders,name='view_search_orders'),
    url(r'^view/order/returnsearch/$',views.get_search_orders,name='get_search_orders'),
    url(r'^view/order/returnsearch/(?P<search>.*)$',views.get_search_orders),
    url(r'^view/order/outstanding/$',views.view_outstanding_orders,name='view_outstanding_orders'),
    url(r'^view/order/(?P<order_id>[0-9]+)/$',views.view_order,name='view_order'),
    url(r'^view/order/(?P<order_id>[0-9]+)/change_status/$',views.change_status,name='change_status'),
    url(r'^view/order/(?P<order_id>[0-9]+)/return/$',views.return_order,name='return_order'),
    url(r'^report/view_all/$', views.view_all),
]
