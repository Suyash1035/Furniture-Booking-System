from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.contrib import messages
from . models import Customer, Payment, Product, Cart, OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

def home(request):
    return render(request,'app/home.html')

def allProducts(request):
    allProducts = Product.objects.all()
    #search
    search_query = request.GET.get('q')
    if search_query :
        allProducts = allProducts.filter(
            Q(title__icontains = search_query)|
            # Q(description__icontains= search_query) |
            Q(category__icontains= search_query)).distinct()
    context = {
        'allProducts' : allProducts,
    }
    return render(request,'app/allproducts.html',context)

def checkout(request):
    return render(request,'app/checkout.html')

#def login(request):
#    return render(request,'app/login.html')

#def signup(request):
 #   return render(request,'app/signup.html')
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        context = {
            'form':form
        }
        return render(request, 'app/signup.html',context)
        
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,"User Registered")
            form.save()
        context = {
            'form':form
        }
        return render(request, 'app/signup.html',context)

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = len(Cart.objects.filter(user=request.user))
        context = {
            'form' : form,
            'totalitem' : totalitem,
            'active' : 'btn-primary'
        }
        return render(request, 'app/profile.html',context)
    
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congrulations. Profile Updated Successfully")
        return render(request, 'app/profile.html',{'form':form,'totalitem':len(Cart.objects.filter(user=request.user)),'active':'btn-primary'})


        #return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        if cart:
            amount = 0.0
            shipping_amount = 70.0
            for p in cart:
                tempamount =(p.quantity * p.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipping_amount
            totalitem = len(cart)

            context = {
                'carts' : cart,
                'totalamount' : totalamount,
                'amount' : amount,
                'totalitem' : totalitem
            }    
            return render(request, 'app/addtocart.html',context)
        else:
            return render(request, 'app/emptycart.html')  

@login_required
def add_to_cart(request):
    user = request.user
    #product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=request.GET.get('prod_id'))
    Cart(user=user,product=product).save()
    return redirect("/cart")
    #return render(request, 'app/addtocart.html')

def plus_cart(request):
    print("In Plus cart")
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        totalamount = amount+shipping_amount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        totalamount = amount+shipping_amount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

# @login_required
# def buy_now(request):
#     user = request.user
#     #product_id = request.GET.get('prod_id')
#     product = Product.objects.get(id=request.GET.get('prod_id'))
#     Cart(user=user,product=product).save()
#     return redirect("/checkout")

# @login_required
# def show_cart(request):
#         if request.user.is_authenticated:
#             user=request.user
#             cart=Cart.objects.filter(user=user)
#         #return render(request,'app/addtocart.html',{'carts':cart})
#         amount=0.0
#         shipping_amount=70.0
#         cart_product=[p for p in Cart.objects.all() if p.user==user]
#         #print(cart_product)
#         if cart_product:
#             for p in cart_product:
#                 tempamount=(p.quantity*p.product.discounted_price)
#                 amount+=tempamount
#                 totalamount=amount+shipping_amount
#                 totalitem=len(Cart.objects.filter(user=request.user))
#             return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
#         else:
#             return render(request,'app/Emptycart.html')

#@login_required
#def add_to_cart(request):
 #   user = request.user
  #  # product_id = request.GET.get('prod_id')
   # product = Product.objects.get(id=request.GET.get('prod_id'))
    #Cart(user=user,product=product).save()
 #   return redirect("/cart")
    #return render(request, 'app/addtocart.html')

# def plus_cart(request):
    #  if request.method=='GET':
    #     prod_id=request.GET['prod_id']
    #     c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    #     c.quantity+=1
    #     c.save()
    #     amount=0.0
    #     shipping_amount=70.0
    #     cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    #     for p in cart_product:
    #         tempamount=(p.quantity*p.product.discounted_price)
    #         amount+=tempamount
    #     totalamount = amount+shipping_amount
    #     data={
    #         'quantity':c.quantity,
    #         'amount':amount,
    #         'totalamount':totalamount
    #     }
    #     return JsonResponse(data)


# def minus_cart(request):
#     if request.method=='GET':
#         prod_id=request.GET['prod_id']
#         c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity -= 1
#         c.save()
#         amount=0.0
#         shipping_amount=70.0
#         cart_product=[p for p in Cart.objects.all() if p.user==request.user]
#         for p in cart_product:
#             tempamount=(p.quantity*p.product.discounted_price)
#             amount+=tempamount
#         totalamount = amount+shipping_amount
#         data={
#             'quantity':c.quantity,
#             'amount':amount,
#             'totalamount':totalamount
#         }
#         return JsonResponse(data)

# def remove_cart(request):
# 	if request.method == 'GET':
# 		prod_id = request.GET['prod_id']
# 		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
# 		c.delete()
# 		amount = 0.0
# 		shipping_amount= 70.0
# 		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
# 		for p in cart_product:
# 			tempamount = (p.quantity * p.product.discounted_price)
# 			# print("Quantity", p.quantity)
# 			# print("Selling Price", p.product.discounted_price)
# 			# print("Before", amount)
# 			amount += tempamount
# 			# print("After", amount)
# 		# print("Total", amount)
# 		data = {
# 			'amount':amount,
# 			'totalamount':amount+shipping_amount
# 		}
# 		return JsonResponse(data)
	

# def remove_cart(request):
#     if request.method=='GET':
#         prod_id=request.GET['prod_id']
#         c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.delete()
#         amount=0.0
#         shipping_amount=70.0
#         cart_product=[p for p in Cart.objects.all() if p.user==request.user]
#         for p in cart_product:
#             tempamount=(p.quantity*p.product.discounted_price)
#             amount+=tempamount
#         data={
#             'amount':amount,
#             'totalamount':amount+shipping_amount
#         }
#         return JsonResponse(data)



def about(request):
    return render(request,'app/about.html')

# def add_to_cart(request):
#     return render(request,'app/addtocart.html')

def bar_stools(request):
    barstools = Product.objects.filter(category='bs')
    context = {
        'barstools' : barstools,
    }
    return render(request,'app/barstoles.html',context)

def beds(request):
    bed = Product.objects.filter(category='b')
    context = {
        'bed' : bed,
    }
    return render(request,'app/beds.html',context)

def bed_side_table(request):
    bedside = Product.objects.filter(category='bst')
    context = {
        'bedside' : bedside,
    }
    return render(request,'app/bedsidetable.html',context)

def book_shelf(request):
    bookshelf = Product.objects.filter(category='bsl')
    context = {
        'bookshelf' : bookshelf,
    }
    return render(request,'app/bookshelf.html',context)

def chaises(request):
    chaises = Product.objects.filter(category='ch')
    context = {
        'chaises' : chaises,
    }
    return render(request,'app/chaises.html',context)

def chestdrawer(request):
    chestdrawer = Product.objects.filter(category='cd')
    context = {
        'chestdrawer' : chestdrawer,
    }
    return render(request,'app/chestdrawer.html',context)

def coffee_table(request):
    coffeetable = Product.objects.filter(category='ct')
    context = {
        'coffeetable' : coffeetable,
    }
    return render(request,'app/coffeetable.html',context)

def king_bed(request):
    kingbed = Product.objects.filter(category='kb')
    context = {
        'kingbed' : kingbed,
    }
    return render(request,'app/kingbed.html',context)

def lounge_chair(request):
    loungechair = Product.objects.filter(category='lc')
    context = {
        'loungechair' : loungechair,
    }
    return render(request,'app/loungechair.html',context)



def product_detail(request):
    return render(request,'app/product-detail.html')

def seatings(request):
    return render(request,'app/seatings.html')

def sofa(request):
    sofas = Product.objects.filter(category='s')
    context = {
        'sofas' : sofas,
    }
    return render(request,'app/sofas.html',context)

def swing(request):
    swing = Product.objects.filter(category='sw')
    context = {
        'swing' : swing,
    }
    return render(request,'app/swing.html',context)

def storage(request):
    return render(request,'app/storages.html')

def study_table(request):
    studytable = Product.objects.filter(category='st')
    context = {
        'studytable' : studytable,
    }
    return render(request,'app/studytable.html',context)

def table(request):
    return render(request,'app/tables.html')

def tv_unit(request):
    return render(request,'app/tvunits.html')

def wall_coverage(request):
    wallcoverage = Product.objects.filter(category='wc')
    context = {
        'wallcoverage' : wallcoverage,
    }
    return render(request,'app/wallcoverage.html',context)

def wall_mount(request):
    wallmount = Product.objects.filter(category='wm')
    context = {
        'wallmount' : wallmount,
    }
    return render(request,'app/wallmount.html',context)

def wooden_dining(request):
    woodendining = Product.objects.filter(category='wd')
    context = {
        'woodendining' : woodendining,
    }
    return render(request,'app/woodendining.html',context)

def modern_dining(request):
    moderndining = Product.objects.filter(category='md')
    context = {
        'moderndining' : moderndining,
    }
    return render(request,'app/moderndining.html',context)
# def order(request):
    # return render(request,'app/orders.html')

#def product_detail(request):

class ProductView(View):
    def get(self,request):
        bar_stools = Product.objects.filter(category='bs')
        sofas = Product.objects.filter(category='s')
        bed_side_table = Product.objects.filter(category='bst')
        book_shelf = Product.objects.filter(category='bsl')
        chaises = Product.objects.filter(category='ch')
        chestdrawer = Product.objects.filter(category='cd')
        coffeetable = Product.objects.filter(category='ct')
        kingbed = Product.objects.filter(category='kb')
        loungechair = Product.objects.filter(category='lc')
        moderndining = Product.objects.filter(category='md')
        studytable = Product.objects.filter(category='st')
        woodendining = Product.objects.filter(category='wd')
        wallcoverage = Product.objects.filter(category='wc')
        wallmount = Product.objects.filter(category='wm')
        swing = Product.objects.filter(category='sw')
        
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        # products = Product.objects.all()
        
        context = {
            'bar_stools' : bar_stools,
            'sofas' : sofas,
            'bed_side_table' : bed_side_table,
            'book_shelf' : book_shelf,
            'chaises' : chaises,
            'chestdrawer' : chestdrawer,
            'coffeetable' : coffeetable,
            'kingbed' : kingbed,
            'loungechair' : loungechair,
            'moderndining' : moderndining,
            'studytable' : studytable,
            'woodendining' : woodendining,
            'wallcoverage' : wallcoverage,
            'wallmount' : wallmount,
            'swing' : swing,
        }
        return render(request,'app/product-detail.html',context)





class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        
        
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        context = {
            'product' : product,
            'item_already_in_cart' : item_already_in_cart,
            'totalitem' : totalitem,
        }
        return render(request, 'app/product-detail.html',context)

def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def checkout(request): 
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    totalitem = len(cart_items)
    amount = 0.0
    shipping_amount = 70.0
    for p in cart_items:
        tempamount =(p.quantity * p.product.discounted_price)
        amount += tempamount
    totalamount = amount + shipping_amount
    context = {
        'add' : add,
        'totalamount' : totalamount,
        'totalitem' : totalitem,
        'cart_items' : cart_items,
        'amount' : amount
    }
    return render(request, 'app/checkout.html',context)

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user = request.user)
    add=Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    context = {
        'order_placed' : op,
        'add' : add,
        'totalitem' : totalitem,
    }
    return render(request, 'app/orders.html',context)


@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        Payment(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

