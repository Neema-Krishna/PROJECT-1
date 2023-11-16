from django.urls import path,include
from user_app import views

urlpatterns = [
    path('index/',views.IndexView.as_view(),name='index'),
     
    path('',views.LoginView.as_view(),name='login'),
    
    path('signin',views.signin,name='signin'),
    
    path('logoutuser/',views.user_logout,name='logoutuser'),
    
    # path('logoutadmin/',views.admin_logout,name='logoutuser'),
    
    path('homepage/',views.HomepageView.as_view(),name='homepage'),
    
    path('about/',views.AboutView.as_view(),name='about'),
    
    # path('blog/',views.BlogView.as_view(),name='blog'),
    
    path('car/',views.CarView.as_view(),name='car'),
    
    path('car/sort/', views.SortCarView.as_view(), name='car-listing-sort'),
    
    # path('car/mileage/',views.FilterCarView.as_view(),name='car-listing-mileage'),
    
    path('contact/',views.ContactView.as_view(),name='contact'),
    
    # path('cartview/',views.CartView.as_view(),name='cart'),
    
    path('cartview/<int:car_id>/', views.CartView1.as_view(), name='carts'),
    path('cart', views.CartView.as_view(), name='cart'),
    
    
    path('getbrandmodels/',views.ModelsView.as_view(),name='getbrandmodels'),
    # path('searchcarbyname/',views.FilterCarView.as_view(),name='searchcarbyname'),
    
    path('vehiclepayment/<int:id>', views.VehiclePayment.as_view(), name='vehiclepayment'),
    
    # path('payment/', views.homepage, name='payment'),
    
    path('paymenthandler/<int:id>', views.paymenthandler, name='paymenthandler')
    

    
    # path('car-detail/',views.CarDetailView.as_view(),name='car-detail')
    
    
    
]
