import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    #print("GET from {} ".format(url))
    if auth:    
        try:
            # Call get method of requests library with URL and parameters
            
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        except:
            # If any error occurs
            print("Network exception occurred")
            status_code = response.status_code
            print("With status {} ".format(status_code))
            json_data = json.loads(response.text)
    else:
        try:    
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")
            status_code = response.status_code
            print("With status {} ".format(status_code))
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
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers=json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
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
    
    dealerID = kwargs['id']
    #print("Kwargs: ",dealerID)
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerID)
    if json_result:
        # Get the row list in JSON as dealers
        dealers=json_result
        #print('json: ',json_result)
        # For each dealer object
        for dealer in dealers:
            review_obj = DealerReview
            
            review_obj.dealership = dealer["dealership"]
            review_obj.name = dealer["name"]
            review_obj.purchase_date = dealer["purchase_date"]
            review_obj.car_make = dealer["car_make"]
            review_obj.car_model = dealer["car_model"]
            review_obj.review = dealer["review"]
            review_obj.id = dealer["id"]
            #review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
   
    return results
#    return "results"
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/fb0cdda6-2ac5-44b3-95ab-77d1f45726de"
    apikey = "4Jir1a02JZgo2Ub94zppUMojIKVz9GuIV-A0LXlH3yKo"
    
    json_result = get_request(url, text=dealerID, api_key=apikey)

    print(json_result)
    return "response"
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
