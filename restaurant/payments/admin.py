from django.contrib import admin

# Register your models here.
admin.site.site_header="myproject"
admin.site.site_title="Shop"
admin.site.index_title="okeythis"
from .models import Order,Transaction,OrderItem
admin.site.register([Order,OrderItem,Transaction])