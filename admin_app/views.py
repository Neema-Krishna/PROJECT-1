from django.shortcuts import render,redirect
from django.views import View
from user_app.models import Vehicle,Vehicle_name,Brand,Query
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail,settings
# Create your views here.

def admin_logout(request):
    logout(request)
    print('logout')
    # return render(request,'login.html')
    return redirect('login')
    

# class IndexView(View):
#     def get(self,request):
#         all_cars=Vehicle.objects.all()
#         print(all_cars)
#         return render(request,'adminpage/index.html',{'vehiclesadminview':all_cars})
    
class VehicleView(View):
    def get(self,request):
        all_cars=Vehicle.objects.all().order_by('-created')
        print(all_cars)
        return render(request,'adminpage/adminVehicleManage.html',{'vehiclesadminview':all_cars})

class VehicleAdd(View):
     
    def get(self,request,*args,**kwargs):
        v_name=Vehicle_name.objects.values_list('v_name',flat=True).distinct()
        return render(request,'adminpage/addvehicle/index.html', {'v_name':v_name})
    
    def post(self,request):
        vehiclename=request.POST.get('name')
        vin=request.POST.get('vin')
        image=request.FILES.get('image1')
        print('image',image)
        image1=request.FILES.get('image2')
        print('image1',image1)
        # image2=request.POST.get('image3')
        year=request.POST.get('year')
        price=request.POST.get('price')
        geartype=request.POST.get('gear_type')
        mileage=request.POST.get('mileage')
        fueltype=request.POST.get('fuel_type')
        kilometer=request.POST.get('kilometer')
        engine=request.POST.get('engine')
        color=request.POST.get('color')
        
        name=Vehicle_name.objects.get(v_name=vehiclename)
         
        vehicle=Vehicle(name=name,vin_number=vin,image=image,image1=image1,kilometer=kilometer
                        ,year=year,price=price,gear_type=geartype,mileagae=mileage,fueltype=fueltype,
                        engine=engine,color=color,status="Avaliable")
        vehicle.save()
        url = '/adminpage/vehicle_add/'
        resp_body = '<script>alert(" Vehicle is added ");\
                                                            window.location="%s"</script>' % url
        return HttpResponse(resp_body) 
    
    
class VehDelete(View) :   
    def get(self,request,*args,**kwargs):
        id=self.kwargs.get('id')
        vehicle=Vehicle.objects.get(id=id)
        vehicle.delete()
        url = '/adminpage/vehicleview/'
        resp_body = '<script>alert(" Vehicle is deleted ");\
                                                            window.location="%s"</script>' % url
        return HttpResponse(resp_body) 
    
class VehicleUpdate(View):
    def get(self,request,*args, **kwargs):
        id=self.kwargs.get('id')
        data=Vehicle.objects.get(id=id)
        print(data)
        print(kwargs)
        return render(request,'edit.html',{'data':data})

    def post(self,request,*args, **kwargs):
        vehiclename=request.POST.get('name')
        vin=request.POST.get('vin')
        image=request.POST.get('image1')
        print('IMAGE',image)
        image1=request.POST.get('image2')
        image2=request.POST.get('image3')
        year=request.POST.get('year')
        price=request.POST.get('price')
        geartype=request.POST.get('gear_type')
        mileage=request.POST.get('mileage')
        fueltype=request.POST.get('fuel_type')
        kilometer=request.POST.get('kilometer')
        engine=request.POST.get('engine')
        color=request.POST.get('color')
        data=Vehicle.objects.get(id=id)
        data.name=vehiclename
        data.vin_number=vin
        data.image=image
        data.image1=image1
        data.year=year
        data.kilometer=kilometer
        data.mileagae=mileage
        data.gear_type=geartype
        data.fueltype=fueltype
        data.color=color
        data.engine=engine
        data.price=price
        data.save()
        url = '/adminpage/vehicleview/'
        resp_body = '<script>alert(" Vehicle Detail is Updated ");\
                                                            window.location="%s"</script>' % url
        return HttpResponse(resp_body) 
         
        
    
class VehicleName(View):
    
    def get(self, request):
        b_names = Brand.objects.all()
        return render(request, 'adminpage/v_nameadd.html', {'b_name': b_names})
    
    def post(self, request):
        b_name = request.POST.get('bname')
        print('bname : ',b_name)
        v_name = request.POST.get('vname')
        print('vname : ',v_name)
        
        # Get the Brand instance based on the provided brand name
        brand = get_object_or_404(Brand, b_name=b_name)
        print('brand',brand)
        
        # Create a new Vehicle_name instance with the brand instance
        name = Vehicle_name(brand_name=brand, v_name=v_name)
        name.save()
        
        url = '/adminpage/v_nameadd/'
        resp_body = '<script>alert("Vehicle Name is added"); window.location="%s"</script>' % url
        return HttpResponse(resp_body)

class BrandName(View):
    
    def get(self, request):
    
        return render(request, 'adminpage/b_nameadd.html')
    
    def post(self, request):
        b_name = request.POST.get('bname')
        print('bname : ',b_name)
        
       # Create a new Vehicle_name instance with the brand instance
        name = Brand(b_name=b_name)
        name.save()
        
        url = '/adminpage/b_nameadd/'
        resp_body = '<script>alert("Brand Name is added"); window.location="%s"</script>' % url
        return HttpResponse(resp_body)

class Enquiry(View):
    def get(self,request):
        query=Query.objects.all()
        return render(request, 'adminpage/enquiry.html' , {'enquiry':query})
class EnquiryReply(View):
    def get(self,request,*args,**kwargs):
        id=self.kwargs.get('id')
        data=Query.objects.get(id=id)
        return render(request,'adminpage/enquiryreply.html',{'data':data})
    
    def post(self,request,*args,**kwargs):
        id=self.kwargs.get('id')
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        to=request.POST.get("email") 
        print(to)
        res=send_mail(subject,message,settings.EMAIL_HOST_USER,[to])
        print("res:",res)
        if res==1:
            url = '/adminpage/enquiryreply/'
            resp_body = '<script>alert("Mail send successfully"); window.location="%s"</script>' % url
            return HttpResponse(resp_body)
        else:
            url = '/adminpage/enquiryreply/'
            resp_body = '<script>alert("Something went wrong"); window.location="%s"</script>' % url
            
            return HttpResponse(resp_body)

class VehicleDetailView(View):
    def get(self,request,**kwargs):
        id=self.kwargs.get('id')
        vehicle=Vehicle.objects.get(id=id)
        
        return render(request,'adminpage/vehicledetail.html',{'vehicle':vehicle})

class Booking(View):
    def get(self,request):
        return render(request, 'adminpage/booking.html')




 
        