import requests
import json
# import related models here
from .models import CarDealer, DealerReview, CarMake, CarModel, ReviewPost
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

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    # URLs are changing periodically, so alternating comment-out
    # url =  "https://starcat7-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
    url =  "https://starcat7-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
    response = requests.post(url, params=kwargs, json=json_payload)
    return response

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
    print(json_result, "96")
    if json_result:
        if isinstance(json_result, list):  # Check if json_result is a list
            reviews = json_result
        else:
            reviews = json_result["data"]["docs"]

        # Check if 'reviews' is a list of one dictionary
        if isinstance(reviews, list) and len(reviews) == 1 and isinstance(reviews[0], dict):
            reviews = reviews[0]

        for dealer_review in reviews:
            print("dealer_review--------------------", dealer_review)  # Print dealer_review
            if isinstance(dealer_review, str):  # Check if dealer_review is a string
                try:
                    dealer_review = json.loads(dealer_review)
                except json.JSONDecodeError:
                    continue  # Skip this iteration if the JSON decoding fails

            review_obj = DealerReview(
                dealership=dealer_review.get("dealership"),
                name=dealer_review.get("name"),
                purchase=dealer_review.get("purchase"),
                review=dealer_review.get("review"),
            )

            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results

# Note: Adjust the keys based on the actual structure of the API response
# MY note: The above code from the point up to the commented out section is to be tinkered with

# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function

# def get_dealer_by_id_from_cf(url, dealerId):

def get_dealer_by_id_from_cf(url, id):

    json_result = get_request(url, id=id)

    if json_result:

        dealers = json_result
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc.get("short_name"))

    return dealer_obj

# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/3161aa14-bc9f-4e30-b8d4-8d6e806f0eb6"
    api_key = "KxhafES4m3v4QJ800EoicmSxs0QiJC8P5britq5Pc4Kc"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    
    # Analyze sentiment
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions())
    ).get_result()

    # Extract sentiment label
    label = response['sentiment']['document']['label']

    return label
"""
def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/3161aa14-bc9f-4e30-b8d4-8d6e806f0eb6"
    api_key = "KxhafES4m3v4QJ800EoicmSxs0QiJC8P5britq5Pc4Kc"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions())).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    
    
    return(label)
"""