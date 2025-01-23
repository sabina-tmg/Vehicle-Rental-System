from django.urls import path, include
from mainApp.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',homepage,name='home'),
    path('about/', about_page, name='about'),

    # Profile
    path('customer_details/', customer_details, name='customer_details'),
    path('owner_details/', owner_details, name='owner_details'),
    path('admin_home/', admin_home, name='admin_home'),
    
    # dashboard configs
    # customer dashboard
    path('rent_page/<int:id>', rent_page, name='rent_page'),
    path('renting/', renting, name='renting'),

    # khalti payment integration
    path('initiate/',initkhalti,name="initiate"),
     path('verify/',verifyKhalti,name="verify"),

    # owner dashboard
    path('vehicle_on_rent/', vehicle_on_rent, name='vehicle_on_rent'),
    path('on_leash/', on_leash, name='on_leash'),
    path('returned_leash/<int:id>', returned_leash, name='returned_leash'),
    path('vehicle/update/<int:id>/', vehicle_update, name='vehicle_update'),
    path('vehicle_register/', vehicle_register, name='vehicle_register'),
    path('delete/<int:id>',vehicle_delete,name='vehicle_delete'),

    # review and rating

    # categories
    path('category/', category_all, name='all_category'),
    path('vehicle/<int:id>', vehicle, name='vehicle'),
    path('individual_category/<str:space>', category_individual, name='individual_category'),
    path('all_vehicles/', all_vehicles, name='all_vehicles'),
    path('search_vehicle/', search_vehicle, name='search_vehicle'),

    # access deny pages
    path('auth_denied/', auth_denied, name='auth_denied'),
    path('customer_needed/', customer_needed, name='customer_needed'),


    # auth section
    path('login/', login_view, name='login_view'),
    path('register/', register, name='register'),
    path('logout/',log_out,name='logout'),
    
]
