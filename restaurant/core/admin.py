from django.contrib import admin
from .models import Category,Momo,Testemonial
# Register your models here.

admin.site.register(Category)
admin.site.register(Testemonial)
from django.utils.html import format_html

@admin.register(Momo)
class MomoAdmin(admin.ModelAdmin):
    list_display=['id','name','price','category','display_img']
    # list_display_links=['name']
    list_editable=['name']
    list_filter=['price','category']
    search_fields=['name']
    # list_per_page=2 
    ordering=['name']
    
    def display_img(self,obj):
        if obj.image:
            return format_html('<img src="{}" height="100px" width="100px">',obj.image.url)