from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from user_app.models import Contact, Brand, MyUser_registration,Vehicle,Query,Vehicle_name,Cart,Booking
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
 

# Create your views here.

def signin(request):
   print('signin')
   if request.user.is_authenticated:
       print('auth')

       if request.user.user_type == 'admin':
           print('admin')
           return render(request,'adminpage/adminhome.html')
       elif request.user.user_type == 'user':
           print(request.user)
           usr=request.session['uid']
           usrr=MyUser_registration.objects.get(id=usr)
           print(usrr.name)
           return redirect('homepage')
        

   return redirect('login')

def user_logout(request):
    logout(request)
    return redirect('login')
    


class IndexView(View):
    def get(self,request):
        return render(request,'index.html')
    
    def post(self,request):
         
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2=request.POST.get('re_password')
        contact=request.POST.get('phone')
        
        if MyUser_registration.objects.filter(email=email).exists():
            url = '/'
            resp_body = '<script>alert("Email already exist!");\
                                                window.location="%s"</script>' % url
            return HttpResponse(resp_body)  
        #    return render(request, 'index.html', { 'error_message': 'Username already taken!'})
        

        
        registration = MyUser_registration(
            username=email,
            first_name=firstname,
            last_name=lastname,
            email=email,
            password=make_password(password),
            phone=contact,
            user_type="user"
        )
        registration.save()
         
        url = '/login/'
        resp_body = '<script>alert("Registration Successfull!");\
                                                            window.location="%s"</script>' % url
        return HttpResponse(resp_body)

        
    
    
class LoginView(View):
    
    def get(self, request):
        return render(request, 'login.html') 
    
    @csrf_exempt
    def post(self,request):
         

        email = request.POST.get('username')
        password = request.POST.get('password')
        print(email)
        print(password)
        # print(Login.objects.all())
        try:
            usr = MyUser_registration.objects.get(email=email)
        except :
            usr = None
        print(usr)

        if(usr):
            print('email exists')
            # user = authenticate(request, email=usr.email, password=password)
            user = authenticate(username=usr.username, password=password)
            
            print("user",user)
            if user is not None:
                usertype = user.user_type

                if usertype == "admin":
                # return render(request, 'labadmin/admindash.html')
                    login(request, user)
                    # return redirect('admindash')
                    return render(request,'adminpage/adminhome.html')

                elif usertype == "user":
                    # return render(request, 'labadmin/admindash.html')
                    print('user_id',usr.id)
                    login(request, user)
                    
                    request.session['uid']=usr.id
                    request.session['uemail']=usr.email
                    return redirect('homepage')
                    # return render(request, 'homepage/index.html',{'user':email,'firstname':usr.first_name,'lastname':usr.last_name}) 


                else:
                    return HttpResponse('Unknown user type')
            else:
                url = '/'
                resp_body = '<script>alert("Wrong password...");\
                                                                window.location="%s"</script>' % url
                return HttpResponse(resp_body)

                # return HttpResponse('Wrong password')
            # print("***")
            # print(usr.email)
            # print(usr.password)
            # if user is not None:
            #     print('success')
            # else:
            #     print('invalid user')
        else:
            url = '/'
            resp_body = '<script>alert("Invalid user...");\
                                                            window.location="%s"</script>' % url
            return HttpResponse(resp_body)
        
class HomepageView(View):
    
    
    def get(self, request):
        active_page = 'home'
        print(f"Active Page: {active_page}")
        user=self.request.user
        print(user.first_name)
        
        Cars=Vehicle.objects.all().order_by('-created')[:4]
        # print(self.email)
        return render(request, 'homepage/index.html',context={"cars":Cars,"user":user,'active_page': active_page}) 
        
class AboutView(View):
    
    def get(self, request):
        active_page = 'about'
        print(f"Active Page: {active_page}")
        return render(request, 'homepage/about.html',{'active_page': active_page})
    
    def post(self,request):
        user=self.request.user
        print(user)
        usr=MyUser_registration.objects.get(email=user)
        print(usr)
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        location=request.POST.get('location')
        service=request.POST.get('service')
        
        Contactdetails=Contact(user_id=usr.id,phone=phone,name=name,location=location,service=service)
        
        Contactdetails.save()
        url = '/about/'
        resp_body = '<script>alert("Sucessfully submitted, we  will reach out to  you!");\
                                                            window.location="%s"</script>' % url
        return HttpResponse(resp_body)
 
class CarView(View):
    
    def get(self, request):
        active_page = 'car'
        print(f"Active Page: {active_page}")

        all_cars = Vehicle.objects.all()  
        paginator = Paginator(all_cars, 6)  
        page = request.GET.get('page')
        print('page:',page)
        try:
            cars1 = paginator.page(page)
            # print(cars1)
        except PageNotAnInteger:
            cars1 = paginator.page(1)
            print('cars1',cars1)
        except EmptyPage:
            cars1 = paginator.page(paginator.num_pages)
            
        brands=Brand.objects.all()
        print("$$$$")    
        print(brands)
        color=Vehicle.objects.values_list('color',flat=True).distinct()
        print(color)

        return render(request, 'homepage/car.html', {'cars1': cars1, 'active_page': active_page,'brands':brands,'color':color})
    
    def post(self,request,*args,**kwargs):
        active_page = 'car'
        cname=request.POST.get('cname')
        cartnameid=request.POST.get('carnamehidden')
        print('id=',cartnameid)
        print('cnamesearch',cname)
        if cname is not None:
            similar_cars = Vehicle.objects.filter(name__v_name__icontains=cname)
        else:
            similar_cars = Vehicle.objects.all()
        Cart=Vehicle.objects.filter(id=cartnameid) 
        print('CartVehicles:',Cart)   
        
        request.session['cars_in_cart'] = cartnameid
        print( 'Similar Cars:',similar_cars)
        
        
        paginator = Paginator(similar_cars, 6)  # 6 cars per page (adjust as needed)
        page = request.GET.get('page')
        try:
            similar_cars = paginator.page(page)
        except PageNotAnInteger:
            similar_cars = paginator.page(1)
        except EmptyPage:
            similar_cars = paginator.page(paginator.num_pages)

        # return render(request, 'homepage/car.html', {'cars1': cars1})
        return render(request, 'homepage/car.html', {'cars1': similar_cars, 'active_page': active_page})
    
    
# class CartView(CarView):
     
#     def get(self, request, *args, **kwargs):
#         active_page = 'cart'
#         cart_vehicles = []
#         user=self.request.user
#         # Retrieve the selected car from the session
#         cartnameid = request.session.get('cars_in_cart')
#         # cars_in_cart = None

#         if cartnameid is not None:
#             try:
#                 cars_in_cart=Vehicle.objects.get(id=cartnameid)
#                 print('Cart:',cars_in_cart)
#                 cart_vehicles.append(cars_in_cart)
#                 Carincart=Cart(user=user,vehicle_cart=cars_in_cart)
#                 Carincart.save()
#             except Vehicle.DoesNotExist:
#             # Handle the case where the car with the provided ID doesn't exist.
#             # You can add error handling or display a message to the user.
#                 pass
            
            
#         return render(request, 'homepage/cart.html', {'cart': cart_vehicles,'active_page': active_page})

class CartView1(View):
    def get(self, request, *args, **kwargs):
        active_page='cart'
        car_id=self.kwargs['car_id']
        user=self.request.user
        cart1=Cart(user=user,vehicle_cart_id=car_id)
        print('cart:',cart1)
        cart1.save()
        
        url = '/car/'
        resp_body = '<script>alert("Added to Cart!");\
                                                    window.location="%s"</script>' % url
        return HttpResponse(resp_body)
        
class CartView(View):
    def get(self, request, *args, **kwargs):
        active_page='cart'
        user=self.request.user
        all_cars = Cart.objects.filter(user=user)  
        paginator = Paginator(all_cars,3)  
        print("paginator",paginator)
        page = request.GET.get('page')
        print('page:',page)
        try:
            cars1 = paginator.page(page)
            print("cars1",cars1)
        except PageNotAnInteger:
            cars1 = paginator.page(1)
            print('cars1',cars1)
        except EmptyPage:
            cars1 = paginator.page(paginator.num_pages)
            
        brands=Brand.objects.all()
        print("$$$$")    
        # print(brands)
        # color=Vehicle.objects.values_list('color',flat=True).distinct()
        # print(color)

        return render(request, 'homepage/cart.html', {'cars1': cars1, 'active_page': active_page,'brands':brands})

        
        
        
     
        

class SortCarView(View):
    
    def get(self, request):
        # Default value setting of sort_param to empty string
        sort_param = request.GET.get('sort', '') 
        
        # Get the sorting parameter from the URL
        sort_param = request.GET.get('sort')

        if sort_param == 'lowest':
            cars = Vehicle.objects.all().order_by('price')
            print('Sorting by lowest')
        elif sort_param == 'highest':
            cars = Vehicle.objects.all().order_by('-price')
            print('Sorting by highest')
        else:
            # Handle cases where no sorting parameter is provided
            cars = Vehicle.objects.all()

        # Pagination logic
        paginator = Paginator(cars, 6)  # 6 cars per page (adjust as needed)
        page = request.GET.get('page')
        try:
            cars1 = paginator.page(page)
        except PageNotAnInteger:
            cars1 = paginator.page(1)
        except EmptyPage:
            cars1 = paginator.page(paginator.num_pages)

        return render(request, 'homepage/car.html', {'cars1': cars1,'sort_param': sort_param})
        
        
 

class ContactView(View):
    
    def get(self, request):
        
        active_page = 'contact'
        print(f"Active Page: {active_page}")
        return render(request, 'homepage/contact.html',{'active_page': active_page}) 
    
    def post(self,request):
        user=self.request.user
        print(user)
        usr=MyUser_registration.objects.get(email=user)
        print(usr)
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        question=request.POST.get('question')
        
        Querydetails=Query(user_id=usr.id,subject=subject,Your_question=question)
        
        Querydetails.save()
        url = '/contact/'
        resp_body = '<script>alert("Sucessfully submitted, we  will reach out to  you!");\
                                                            window.location="%s"</script>' % url
        return HttpResponse(resp_body)
        
        # return redirect('contact')
        
        
        
class ModelsView(View):
    def get(self,request):  
        brand_id=request.GET['brand_id'] 
        print(brand_id) 
        result=Vehicle_name.objects.filter(brand_name_id=brand_id)
        print(result)
        jsonData=serialize('json',result)
        print(jsonData)
       
        return JsonResponse({"status":"sucesss","models":jsonData})
     
     
     
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

class VehiclePayment(View):
    def get(self,request,**kwargs):
        print('payment1')
        id=self.kwargs.get('id')
        vehicle=Vehicle.objects.get(id=id)
        currency = 'INR'
        amount =  (vehicle.price*25)
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['car']=vehicle
        print('payment')
        return render(request,'vehiclepayment.html',context)
    
 
 
# def homepage(request):
#     currency = 'INR'
#     amount = 20000  # Rs. 200
 
#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))
 
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'
 
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
 
#     return render(request, 'homepage/payment.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request,**kwargs):
 
    # only accept POST request.
    if request.method == "POST":
        id=kwargs.get('id')
        user=request.user
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    booking=Booking(user=user,vehicle_booked_id=id,status="Booked")
                    booking.save()
                    vehicle_booked=Vehicle.objects.get(id=id)
                    vehicle_booked.status="Booked"
                    vehicle_booked.save()
                    
                    # render success page on successful caputre of payment
                    return HttpResponse("Success")
                except:
 
                    # if there is an error while capturing payment.
                    return HttpResponse("Failed")
            else:
 
                # if signature verification fails.
                return HttpResponse("Invalid Credentials")
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

                
    
         
   
    
    