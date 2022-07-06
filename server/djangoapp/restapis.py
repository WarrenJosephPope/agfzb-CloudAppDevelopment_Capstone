import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print("GET from {}".format(url))
    try:
        response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)
        status_code = response.status_code
        print("With status {}".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print("Network exception occured: ",e)

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("POST from {}".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        print("With status {}".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print("Network exception occured: ",e)

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        dealers = json_result["result"]
        for dealer_doc in dealers:
            dealer_obj = CarDealer(address=dealer_doc['address'],city=dealer_doc['city'], full_name=dealer_doc['full_name'], id=dealer_doc['id'], lat=dealer_doc['lat'], lon=dealer_doc['long'], short_name=dealer_doc['short_name'], st=dealer_doc['st'], state=dealer_doc['state'], zip_code=dealer_doc['zip'])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, id=dealer_id)
    if json_result:
        review = json_result["result"]
        for review_doc in review:
            if review_doc['purchase'] == True:
                review_obj = DealerReview(dealership=review_doc['dealership'],name=review_doc['name'], purchase=review_doc['purchase'], review=review_doc['review'], purchase_date=review_doc['purchase_date'], car_make=review_doc['car_make'], car_model=review_doc['car_model'], car_year=review_doc['car_year'], id=review_doc['id'])
            else:
                review_obj = DealerReview(dealership=review_doc['dealership'],name=review_doc['name'], purchase=review_doc['purchase'], review=review_doc['review'], id=review_doc['id'])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text): 
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/8be68ed5-4b2f-4658-94dd-e14c3c113638"
    api_key = "kqwr7w_ZbhMqvyvJqp8o54T_J-dCBiyEBRBo19tQYZgU"
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 
    response = natural_language_understanding.analyze( text=text, language="en", features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 
    label=json.dumps(response, indent=2) 
    label = response['sentiment']['document']['label']
    return(label) 
