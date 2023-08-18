import os
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview, CarModel, CarMake
from .restapis import get_request, get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        
        url = os.environ['COUCH_getDealers_URL'] 
        # Get dealers from the URL
        #dealerships = get_dealers_from_cf(url)
        dealerships = get_dealers_from_cf(url, id = 0)
        # Return a list of dealer short name
        context['dealership_list'] = dealerships

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}

        url = os.environ['COUCH_getReviews_URL'] 
        reviews = get_dealer_reviews_from_cf(url, id=dealer_id)

        url = os.environ['COUCH_getDealers_URL'] 
        dealership = get_dealers_from_cf(url, id=dealer_id)
        
        context['reviews'] = reviews
        context['dealership'] = dealership

        return render(request, 'djangoapp/dealer_details.html', context)
        #return HttpResponse(dealer_reviews)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    user = request.user
    #dealer_id = kwargs["dealer_id"]

    
    if user.is_authenticated:
        if request.method == 'GET':
            context = {}

            url = os.environ['COUCH_getDealers_URL'] 
            dealership = get_dealers_from_cf(url, id=dealer_id)
            
            dealer_name =' '.join([dealer.full_name for dealer in dealership])
            
            cars = CarModel.objects.filter(dealerID=dealer_id)

            context['dealership'] = dealership
            context['dealer_id'] = dealer_id
            context['dealer_name'] = dealer_name
            context['cars'] = cars

            return render(request, 'djangoapp/add_review.html', context)   
        elif request.method == 'POST':
            review = {}
            json_payload = {}

            url = os.environ['COUCH_getDealers_URL'] 
            dealership = get_dealers_from_cf(url, id=dealer_id)
            
            dealer_name =' '.join([dealer.full_name for dealer in dealership])

            url = os.environ['COUCH_postReview_URL']
            purchase = request.POST.get('purchasecheck')
            if purchase:
                review["purchase"] = True
            else:
                review["purchase"] = False

            car = request.POST["car"]
            car = car.split('-')
            review["car_model"] = car[0]
            review["car_make"] = car[1]
            review["car_year"] = car[2]

            review["name"] = user.username
            review["time"] = datetime.utcnow().isoformat()
            review["purchase_date"] = request.POST["purchasedate"]
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]

            json_payload["review"] = review

            response = post_request(url, json_payload)

            
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        return HttpResponse(403)
# ...
