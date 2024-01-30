import requests
import json
# import related models here
from .models import CarDealer, DealerReview, CarMake, CarModel
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time
 

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
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
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
"""
Considering replacing the above code with the code below that was given in instructions
import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
"""
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
#def get_dealers_from_cf(url, **kwargs):
#    results = []
#    state = kwargs.get("state")
#    if state:
#        json_result = get_request(url, state=state)
#    else:
#        json_result = get_request(url)

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)

    if json_result and "body" in json_result and "data" in json_result["body"]:
        reviews = json_result["body"]["data"]

        for dealer_review_data in reviews:
            # Assuming "docs" is the list of reviews
            if "docs" in dealer_review_data:
                for review_data in dealer_review_data["docs"]:
                    review_obj = DealerReview(
                        dealership=review_data.get("dealership", ""),
                        name=review_data.get("name", ""),
                        purchase=review_data.get("purchase", False),
                        review=review_data.get("review", "")
                    )

                    if "id" in review_data:
                        review_obj.id = review_data["id"]
                    if "purchase_date" in review_data:
                        review_obj.purchase_date = review_data["purchase_date"]
                    if "car_make" in review_data:
                        review_obj.car_make = review_data["car_make"]
                    if "car_model" in review_data:
                        review_obj.car_model = review_data["car_model"]
                    if "car_year" in review_data:
                        review_obj.car_year = review_data["car_year"]

                    # Analyze sentiment
                    sentiment = analyze_review_sentiments(review_data.get("review", ""))
                    review_obj.sentiment = sentiment

                    results.append(review_obj)

    return results

"""

def get_dealers_from_cf(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        dealerships_data = response.json()

        dealerships = []
        for dealer_doc in dealerships_data:
            # Assuming each dealer_doc is a dictionary with relevant keys
            dealer_obj = CarDealer(
                address=dealer_doc.get("address", ""),
                city=dealer_doc.get("city", ""),
                full_name=dealer_doc.get("full_name", ""),
                id=dealer_doc.get("id", ""),
                lat=dealer_doc.get("lat", ""),
                long=dealer_doc.get("long", ""),
                short_name=dealer_doc.get("short_name", ""),
                st=dealer_doc.get("st", ""),
                zip=dealer_doc.get("zip", "")
            )
            dealerships.append(dealer_obj)

        return dealerships
    else:
        # Handle the error or return an empty list
        return []
"""
# Note: Adjust the keys based on the actual structure of the API response
# MY note: The above code from the point up to the commented out section is to be tinkered with

# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
"""
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)

    if json_result:
        reviews = json_result["body"]["data"]["docs"]

        for dealer_review in reviews:
            #dealer_review = reviews
            reviews = json_result["body"]["data"]["docs"]

        for dealer_review_data in reviews:
            print("Dealer Review Data:", dealer_review_data)
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])

            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]

            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)
    return results
            """




# def get_dealer_by_id_from_cf(url, dealerId):
"""
def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
   
    if json_result:
        dealers = json_result["body"]
        dealer_doc = dealers["docs"][0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],                                
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
        
    return dealer_obj
"""
def get_dealer_by_id_from_cf(url, id):

    json_result = get_request(url, id=id)

    if json_result:

        dealers = json_result

        dealer_doc = dealers[0]

        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],

                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],

                                st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc.get("short_name"))

    return dealer_obj
"""
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc.get("short_name"))
    return dealer_obj
"""
"""
    if json_result:
        dealers = json_result
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc.get("short_name"))
    return dealer_obj
"""
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
"""def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/c8b0f019-31d6-41ac-b003-a2a31608839e"
    api_key = "X2W_XG21E2BqmQ57cKeaX1rI9N43ZflG2KuaUmPJ_7wq"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    """
def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/c8b0f019-31d6-41ac-b003-a2a31608839e"
    api_key = "X2W_XG21E2BqmQ57cKeaX1rI9N43ZflG2KuaUmPJ_7wq"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    
    # Analyze sentiment
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions(targets=[text]))
    ).get_result()

    # Extract sentiment label
    label = response['sentiment']['document']['label']

    return label
