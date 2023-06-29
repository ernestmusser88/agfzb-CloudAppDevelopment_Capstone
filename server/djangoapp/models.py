from django.db import models
from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100, default='name')
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):

    Car_Types = [
    ("Sedan", "Sedan"),
    ("SUV", "SUV"),
    ("Wagon", "Wagon")
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerID = models.IntegerField(default=0)
    name = models.CharField(null=False, max_length=100, default='name')
    type = models.CharField(null=False, choices=Car_Types, max_length=100, default='name')
    year = models.DateField(null=True)

    def __str__(self):
        return  format(self.name) + ", " + \
                "Make: " + format(self.make.name) + ", " + \
                "Type: " + format(self.type)+ ", " + \
                "DealerID: " + format(self.dealerID)
                

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class CarReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, sentiment, id):
        # Dealer dealership
        self.dealership = dealership
        # Dealer name
        self.name = name
        # Dealer purchase
        self.purchase = purchase
        # Dealer review
        self.review = review
        # Location purchase_date
        self.purchase_date = purchase_date
        # Location car_make
        self.car_make = car_make
        # Dealer car_model
        self.car_model = car_model
        # Dealer sentiment
        self.sentiment = sentiment
        # Dealer id
        self.id = id
    def __str__(self):
        return "Dealer name: " + self.name