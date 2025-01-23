from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import admin_only, owner_only, customer_only
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from uuid import uuid4
from django.http import Http404
from datetime import datetime

date=datetime.now()
# Create your views here.
def homepage(request):
    works = Works.objects.all() # for the working process of the system
    context = {
        'works':works,
        'date':date
    }
    return render(request,'pages/homepage.html',context)

def about_page(request):
    return render(request, 'pages/about.html',{'date':date})


def category_all(request):
        categories = Category.objects.all()
        context = {
                    'categories':categories,
                    'date':date
                }
                
        return render(request, 'category/categories.html', context)



def category_individual(request, space):
    space = space.replace('-', ' ')
    try:
        category = Category.objects.get(name=space)  # Use `get` to retrieve a single object
    except Category.DoesNotExist:
        # Handle the case where the category doesn't exist
        category = None
        vehicles = []
    else:
        vehicles = Vehicles.objects.filter(category=category, isDelete=False)

    context = {
        'vehicles': vehicles,
        'category': category,
        'date':date
    }
    return render(request, 'category/individual_category.html', context)
def all_vehicles(request):
     vehicles = Vehicles.objects.filter(isDelete=False, available = True)
     unavailable_vehicle = Vehicles.objects.filter(isDelete=False, available = False)

     context={
          'vehicles':vehicles,
          'v2':unavailable_vehicle,
          'date':date
     }
     return render(request, 'category/all_vehicles.html', context)

def vehicle(request,id):
    vehicle = Vehicles.objects.get(id=id)
    reviews = vehicle.reviews.all()
    if request.method == 'POST' and request.user.is_customer:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.vehicle = vehicle
            review.user = request.user

            review.save()
            return redirect('vehicle', id=vehicle.id)
    else:
        form = ReviewForm()

    context = {
         'vehicle':vehicle,
         'reviews':reviews,
         'form': form,
         'range':range(1, 6),
         'date':date
    }

    return render(request, 'pages/vehicle.html',context)




# Check if the input is a non-null and non-empty value
def is_valid_queryparam(param):
    return param != '' and param is not None

# Search vehicle plus filter
def search_vehicle(request):
    qs = Vehicles.objects.filter(isDelete=False)
    # categories = Category.objects.all()
    searched = request.GET.get('searched')
    min_rate = request.GET.get('min_rate')
    max_rate = request.GET.get('max_rate')
    category = request.GET.get('category')

    if is_valid_queryparam(searched): # for the model name search
        qs = qs.filter(vehicle_model__icontains=searched)

    if is_valid_queryparam(min_rate):   # minimum rental price
        qs = qs.filter(rent_price__gte=min_rate)

    if is_valid_queryparam(max_rate):   # maximum rental price
        qs = qs.filter(rent_price__lte=max_rate)

    if is_valid_queryparam(category) and category != 'Choose...':   # choose vehicle category
        qs = qs.filter(category__name=category)
    
    return render(request, 'category/search_vehicle.html', {'query': qs, 'searched': searched,'date':date})


# dashboard section start
    


# customer only section
@customer_only
def customer_details(request):
    user_form = UserUpdateForm(instance=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('customer_details')  # Redirect to a page displaying the updated profile

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user,
        'profile': request.user.profile,
        'date':date
    }
    return render(request, 'pages/customer/customer_details.html', context)

@customer_only
def renting(request):
    vehicle = Vehicles.objects.filter(isDelete=False, available = False, rented_by=request.user)
    context = {
        'profile': request.user.profile,
        'vehicle':vehicle,
        'date':date
    }
    return render(request, 'pages/customer/renting.html', context)

@customer_only
def rent_page(request, id):
    vehicle = Vehicles.objects.get(id=id)
    context = {
        "vehicle":vehicle,
        'date':date
    }
    return render(request, 'pages/customer/rent_page.html', context)



# customer only section ends

# owner only section
@owner_only
def owner_details(request):
    user_form = UserUpdateForm(instance=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('owner_details')  # Redirect to a page displaying the updated profile

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user,
        'profile': request.user.profile,
        'date':date
    }

    return render(request, 'pages/owner/owner_details.html', context) 

@owner_only
def vehicle_register(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)  # Do not save to the database yet
            vehicle.uploaded_by = request.user  # Set the uploaded_by field to the current user
            vehicle.save()  # Now save the instance to the database
            return redirect('owner_details')
    else:
        form = VehicleForm()

    context = {
        'profile': request.user.profile,
        'form':form,
        'date':date
    }
    return render(request, 'pages/owner/vehicle_register.html', context)

@owner_only
def vehicle_update(request, id):
    vehicle = Vehicles.objects.get(id=id)  # Retrieve the vehicle instance by primary key

    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()  # Save the updated vehicle instance
            return redirect('vehicle_on_rent')
    else:
        form = VehicleForm(instance=vehicle)  # Populate the form with the existing vehicle data

    return render(request, 'pages/owner/vehicle_update.html', {'form': form,'date':date})


@owner_only
def vehicle_delete(request, id):
    vehicle = Vehicles.objects.get(id=id)  # Retrieve the vehicle instance by primary key
    vehicle.isDelete=True
    vehicle.save()
    return redirect('vehicle_on_rent')


@owner_only
def vehicle_on_rent(request):
    rented_vehicles = Vehicles.objects.filter(uploaded_by=request.user, isDelete=False)
    context={
        'context':'sabina',
        'rented_vehicles': rented_vehicles,
        'profile': request.user.profile,
        'date':date
    }
    return render(request, 'pages/owner/vehicle_on_rent.html', context)


@owner_only
def on_leash(request):
    vehicle = Vehicles.objects.filter(isDelete=False, available = False, uploaded_by=request.user)

    context = {
        'profile': request.user.profile,
        'vehicle':vehicle,
        'date':date
    }
    return render(request, 'pages/owner/on_leash.html', context)


@owner_only
def returned_leash(request, id):
    if request.method == 'POST':
        vehicle = Vehicles.objects.get(id=id, available = False)
        vehicle.available = True
        vehicle.save()
    
    return redirect('on_leash')

# owner only section ends

# admin only section
@admin_only
def admin_home(request):
     return render(request, 'pages/admin/admin_home.html',{'date':date})


# admin only section ends

# access denied section
def auth_denied(request):
     return render(request, 'pages/access/auth_denied.html',{'date':date})

def customer_needed(request):
     return render(request, 'pages/access/customer_needed.html',{'date':date})
# access denied section ends

# dashboard section ends



# auth section start
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user object
            user = form.save()
            # Provide a personalized success message
            messages.success(request, f"Hi '{user.username}' created successfully! You can now log in.")
            return redirect('login_view')  # Redirect to login page after successful registration
        else:
            # Show detailed error messages if the form is not valid
            messages.error(request, "Invalid Form! Please correct the highlighted errors.")
    else:
        form = SignUpForm()

    return render(request, 'auth/register.html', {'form': form,'date':date})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if not User.objects.filter(username=username).exists():
                messages.error(request,"Username doesn't exist")

            elif user is not None and user.is_admin:
                login(request, user)
                messages.success(request, "Welcome Admin")
                return redirect('admin_home')
            elif user is not None and user.is_customer:
                login(request, user)
                messages.success(request, "Welcome customer")
                return redirect('customer_details')
            elif user is not None and user.is_owner:
                login(request, user)
                messages.success(request, "Welcome owner")
                return redirect('owner_details')
            else:
                messages.error(request,"Try again!")
                return redirect('login_view')
        else:
            messages.error(request,"Try again!")
    return render(request, 'auth/login.html', {'form': form, 'msg': msg,'date':date})

@login_required(login_url='login_view')
def change_password(request):
    cf = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        cf = PasswordChangeForm(user=request.user, data=request.POST)
        if cf.is_valid():   #for validation
            cf.save()
            return redirect('login_view')
    return render(request,'auth/change_password.html',{'cf':cf})

def log_out(request):
    logout(request)
    return redirect('login_view')

# auth section end




# Payment section start of kalti:
@csrf_exempt
def initkhalti(request):
    if request.method == 'POST':
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        return_url = 'http://127.0.0.1:8000/verify/'
        amount = 1000
        transaction_id = str(uuid4())  # Generate a unique transaction ID
        purchase_order_name = request.POST.get('vehicle_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        vehicle_id = request.POST.get('vehicle_id')
        owned_by = request.POST.get('owned_by')

        # Generate a unique purchase_order_id
        purchase_order_id = request.POST.get('vehicle_id')

        payload = json.dumps({
            "return_url": return_url,
            "website_url": return_url,
            "amount": 1000,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": purchase_order_name,
            "transaction_id": transaction_id,
            "customer_info": {
                "name": username,
                "email": email,
                "phone": phone,
            },
            "product_details": [
                {
                    "identity": vehicle_id,
                    "name": purchase_order_name,
                    "unit_price": amount,
                    "total_price": amount,
                    "quantity": 1
                }
            ],
            "merchant_username": owned_by,
        })

        headers = {
            'Authorization': 'key bf22686cf11682e29d657b984d138978',
            'Content-Type': 'application/json',
        }

        response = requests.post(url, headers=headers, data=payload)
        new_res = response.json()

        print("Khalti API Response:", new_res)  # Debugging statement

        if response.status_code == 200 and 'payment_url' in new_res:
            return redirect(new_res['payment_url'])
        else:
            return JsonResponse({'error': 'Failed to initiate payment', 'details': new_res}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



# what to do after payment

@csrf_exempt
def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key bf22686cf11682e29d657b984d138978',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
        purchase_order_id = request.GET.get('purchase_order_id')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
            vehicle = get_object_or_404(Vehicles, id=purchase_order_id)
            vehicle.available = False
            vehicle.rented_by = request.user  # Assuming the user is logged in
            vehicle.save()

            RentTransaction.objects.create(
                vehicle=vehicle,
                transaction_id=transaction_id,
                amount=new_res['total_amount'],  # Assuming amount is returned in the response
                user=request.user
            )

            send_mail(
                'Vehicle Rented',
                f'Your vehicle {vehicle.vehicle_model} has been rented by {request.user.username}.',
                'syangtansabina8@gmail.com',
                [vehicle.uploaded_by.email],
                fail_silently=False,
            )
            return redirect('customer_details')
        else:
            print("Payment verification failed. Khalti response:", json.dumps(new_res, indent=4))
            return JsonResponse({'error': 'Payment verification failed'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)