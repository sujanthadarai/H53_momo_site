from django.shortcuts import render,redirect
from .models import Contact,Category,Momo,Testemonial
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import uuid

import hashlib
import uuid
import base64
import json
import hmac
import logging
logger=logging.getLogger("django")

# Create your views here.

def index(request):
    category=Category.objects.all()
    teste=Testemonial.objects.filter(is_active=True)
    cateid=request.GET.get("category")
    momo=None
    data=None
    total=0
    
    try:
        

        if cateid:
            momo=Momo.objects.filter(category=cateid)
        else:
            momo=Momo.objects.all()
            
        paginator=Paginator(momo,2)
        num_p=request.GET.get("page") #http://127.0.0.1:8000/momo?page=2
        data=paginator.get_page(num_p)
        total=data.paginator.num_pages #2
        
        
        if request.method == 'POST':
            name=request.POST['name']
            email=request.POST['email']
            phone=request.POST['phone']
            message=request.POST['message']
            
            Contact.objects.create(name=name,email=email,phone=phone,message=message)
            return redirect('index')
    except Exception as e:
        logger.error(e,exc_info=True)
    
    context={
        'date':datetime.now(),
        "category":category,
        "momo":momo,
        'teste':teste,
        'data':data,
        'num': [i+1 for i in range(total)] #[1,2]
        }
    return render(request,'core/index.html',context)

# @login_required(login_url="log_in")
def about(request):
    return render(request,'core/about.html',{'date':datetime.now()})

@login_required(login_url="log_in")
def menu(request):
    return render(request,'core/menu.html')
def contact(request):
    return render(request,'core/contact.html')
def service(request):
    return render(request,'core/services.html')


''' 
=========================================================
                   Add to Cart
=========================================================

'''


@login_required(login_url="log_in")
def cart_add(request, id):
    cart = Cart(request)
    product = Momo.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="log_in")
def item_clear(request, id):
    cart = Cart(request)
    product = Momo.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def item_increment(request, id):
    cart = Cart(request)
    product = Momo.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def item_decrement(request, id):
    cart = Cart(request)
    product = Momo.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

# singature
def generate_signature(data, secret):
    # signed_field_names must be included in the payload
    signed_fields = data["signed_field_names"].split(",")
    # Create message string in exact order
    message = ",".join([f"{field}={data[field]}" for field in signed_fields])
    signature = hmac.new(
    secret.encode("utf-8"),
    message.encode("utf-8"),
    hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode("utf-8")

@login_required(login_url="log_in")
def cart_detail(request):
    cart=request.session.get("cart")
    amount=0
    for item in cart.values():
        amount+= item['quantity']*float(item['price'])
    amount=round(amount,2)
    tax_amount=round(amount*0.13,2)
    total_amount=round(amount+tax_amount,2)
    print(amount)
    secret_key="8gBm/:&EnhH.1/q"
    
    data={
        "amount":amount,
        "tax_amount":tax_amount,
        "total_amount":total_amount,
        "transaction_uuid":str(uuid.uuid4()),
        "product_code":"EPAYTEST",
        "signed_field_names":"total_amount,transaction_uuid,product_code",
        "success_url":"http://127.0.0.1:8000/payments/success_url/",
        "failure_url":"http://127.0.0.1:8000/payments/failure_url/"
    }
    data['signature']=generate_signature(data,secret_key)
        
    return render(request, 'core/cart.html',data)


# pip freeze > requirements.txt
# pip install -r requirements.txt

'''
Domain Name : human readable address of website 

https//:www.sipalaya.com
https -->protocol : 
www : subdomain
sipalaya.com -->second level domain -->site owner 
.com -->top level domain 


Hosting :renting space on a computer(server)

Type of hosting :
shared host : line on server ,shared 

vps hosting : 
one pyshical server is divided into separeated

Dedicated hosting : 


#cloud hostigg : aws,azure


'''


'''

GIT & GITHUB
GIT : version control system 
it track our all histroy of our project(save,edit,change,save)
coding collaboration

Github : webiste that allow developer to store and manage their data using git

computer(local file ) -->git init -->stage area(git add .) -->local repo(git commit -m "message") --->(git push)github(repo)

'''