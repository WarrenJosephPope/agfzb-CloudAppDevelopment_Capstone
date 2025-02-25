from django.db import models
from django.utils.timezone import now
from django.conf import settings


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=True, max_length=150)
    def __str__(self):
        return self.name
    def get_data(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_CHOICES = [(SEDAN, "Sedan"), (SUV, "SUV"), (WAGON, "Wagon")]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    car_name = models.CharField(null=False, max_length=30, default="")
    car_type = models.CharField(null=False, max_length=30, choices=CAR_CHOICES, default=SEDAN)
    year = models.DateField(default=now)
    def __str__(self):
        return self.car_name
    def get_data(self):
        data = dict()
        data['make'] = self.car_make.get_data()
        data['dealer_id'] = self.dealer_id
        data['name'] = self.car_name
        data['year'] = self.year.strftime('%Y')
        return data

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, lon, short_name, st, state, zip_code):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.lon = lon
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip_code = zip_code

    def __str__(self):
        return "Dealer name: "+self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self,id,name,dealership,review,purchase,sentiment="Neutral",purchase_date=None,car_make=None,car_model=None,car_year=None):
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.sentiment = sentiment
        if purchase == True:
            self.purchase_date = purchase_date
            self.car_make = car_make
            self.car_model = car_model
            self.car_year = car_year
    def __str__(self):
        return "Name: "+self.name
