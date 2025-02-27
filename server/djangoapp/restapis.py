import os
import requests
import json
import asyncio
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    #print(kwargs)
    api_key = kwargs.get("api_key")
    #print("GET from {} ".format(url))
    try:    
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    # print("With status {} ".format(status_code))    
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    if  kwargs['id'] == 0:
        json_result = get_request(url)
    else:
        json_result = get_request(url, id=kwargs['id'])

    if json_result:
        # Get the row list in JSON as dealers
        dealers=json_result
        # For each dealer object
        for dealer in dealers:
            if  kwargs['id'] == 0:#if we're grabbing multiple dealers
                dealer_doc = dealer["doc"]
            else:
                # Get its content in `doc` object
                dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf (url, **kwargs):
    results = []

    review_temp = { "_id": "","_rev": "1-","another": "","car_make": "","car_model": "",
                    "car_year": 0,"dealership": 0,"id": 0,"name": "", "purchase": False,
                    "purchase_date": "","review": ""}

    dealerID = kwargs['id']
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerID)

    if json_result:

        # Get the row list in JSON as reviews
        reviews=json_result

        for review in reviews:
            this_review = review
            for key in this_review.keys():
                review_temp[key] = this_review[key]

            #Populate Model    
            review_obj = DealerReview(dealership = review_temp["dealership"], name = review_temp["name"], purchase_date = review_temp["purchase_date"],
                      car_make = review_temp["car_make"], car_model = review_temp["car_model"], review = review_temp["review"],
                      sentiment = "", purchase = review_temp["purchase"], id = review_temp["id"])

            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            #print(review_obj.sentiment)
            results.append(review_obj)

    return results
#    return "results"
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    label = []
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/cf644e81-0df7-48c2-823c-1cec40dba2bc" 

    api_key = os.environ['NLU_API_KEY'] 
    
    authenticator = IAMAuthenticator(api_key) 
    
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    
    natural_language_understanding.set_service_url(url) 

    try:
        response = natural_language_understanding.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 
        label=json.dumps(response, indent=2)
        label = response['sentiment']['document']['label'] 
    except Exception as err:
        print("Network exception occurred")
        label = "N/A"
       
    
    return(label) 
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def post_request(url, json_payload, **kwargs):

    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))    
    #json_data = json.loads(response.text)
    return status_code
