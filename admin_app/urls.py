from django.urls import path,include
from admin_app import views

urlpatterns = [
    # path('',views.IndexView.as_view(),name='indexadmin'),
    path('vehicleview/',views.VehicleView.as_view(),name='vehiclesadmin'),
    path('adminlogout/',views.admin_logout,name='adminlogout'),
    path('vehicle_add/',views.VehicleAdd.as_view(),name='vehicle_add'),
    path('vehicle_delete/<int:id>/',views.VehDelete.as_view(),name='vehicle_del'),
    path('vehicle_edit/<int:id>/',views.VehicleUpdate.as_view(),name='vehicle_update'),
    path('v_nameadd/',views.VehicleName.as_view(),name='v_nameadd'),
    path('b_nameadd/',views.BrandName.as_view(),name='b_nameadd'),
    path('enquiry/',views.Enquiry.as_view(),name='enquiry'),
    path('booking/',views.Booking.as_view(),name='booking'),
    path('enquiry/<int:id>/',views.EnquiryReply.as_view(),name='enquiryreply'),
    path('vehicleview/<int:id>/',views.VehicleDetailView.as_view(),name='vehicledetail'),
    
    
]