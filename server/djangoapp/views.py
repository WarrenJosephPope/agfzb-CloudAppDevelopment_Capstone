from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
# from .models import related models
from .models import CarMake, CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
# def about(request):
# ...

def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
#def contact(request):

def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
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
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

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
    context = {}
    if request.method == "GET":
        url = "https://58777923.us-south.apigw.appdomain.cloud/api/dealership"
        dealership = get_dealers_from_cf(url)
        context = {"dealership": dealership}
        return render(request, "djangoapp/index.html", context=context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://58777923.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        dealership = get_dealers_from_cf("https://58777923.us-south.apigw.appdomain.cloud/api/dealership", id=dealer_id)
        dealer_name = ""
        for dealer in dealership:
            dealer_name = dealer.full_name
        context = {"reviews": reviews, "dealer_name": dealer_name, "dealer_id": dealer_id}
        return render(request, "djangoapp/dealer_details.html", context=context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.method == "POST":
        review = dict()
        review['name'] = request.POST["name"]
        review['dealership'] = dealer_id
        review['review'] = request.POST["content"]
        if "purchase" in request.POST:
            review['purchase'] = True
        else:
            review['purchase'] = False
        if review['purchase']:
            review['purchase_date'] = request.POST['purchasedate']
            car = request.POST['car']
            car_details = car.split('-')
            review['car_make'] = car_details[0]
            review['car_model'] = car_details[1]
            review['car_year'] = car_details[2]
        json_payload = dict()
        json_payload['review'] = review
        result = post_request("https://58777923.us-south.apigw.appdomain.cloud/api/review", json_payload, dealerId=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        context = dict()
        reviews = get_dealer_reviews_from_cf("https://58777923.us-south.apigw.appdomain.cloud/api/review", dealer_id=dealer_id)
        dealership = get_dealers_from_cf("https://58777923.us-south.apigw.appdomain.cloud/api/dealership", id=dealer_id)
        cars = []
        car_list = CarModel.objects.all().filter(dealer_id=dealer_id)
        for car in car_list:
            cars.append(car.get_data())
            break
        print(cars)
        for dealer in dealership:
            context["dealer_name"] = dealer.full_name
        context["cars"] = cars
        context["dealer_id"] = dealer_id
        return render(request, "djangoapp/add_review.html", context=context)
