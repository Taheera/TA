from __future__ import print_function

import flask
from flask import request, jsonify, make_response
import re, math
from collections import Counter
import json
import pandas as pd
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import os

import google.cloud
from google.cloud import bigquery

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    # commented out by Naresh
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    #if req.get("queryResult").get("action") != "interest":
    if req.get("queryResult").get("action") != "osteo-info":
        return {}
    baseurl = "https://d00c443a.ngrok.io/api/v1/resources/books?questions="
    #yql_query = makeYqlQuery(req)
    #if yql_query is None:
        #return {}
    result = req.get("queryResult")
    parameters = result.get("parameters")
    ques = parameters.get("any")
    ques1 = ques.replace(" ","+")
    yql_url = baseurl + str(ques1)
    result = urlopen(yql_url).read()
    data1 = json.loads(result)
    if len(data1) == 0:
        #print("Response:")
        speech = "please try another question."
        return {
            "fulfillmentText": speech,
            "source": "API"
        }
        #for some the line above gives an error and hence decoding to utf-8 might help
        #data = json.loads(result.decode('utf-8'))
        #res = makeWebhookResult(data)
    else:
        speech = str(data1[0]["answers"])
        #speech = data1
        print("Response:")
        print(speech)
        return {
            "fulfillmentText": speech,
            "source": "API"
        }

@app.route('/test', methods=['GET'])
def test():
    return  "Hello there my friend !!"

@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    string = "You are awesome !!"
    Message ="this is the message"

    my_result =  {

    "fulfillmentText": string,
     "source": string
    }

    res = json.dumps(my_result, indent=4)

    r = make_response(res)

    r.headers['Content-Type'] = 'application/json'
    return r


WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator


def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="Google Project-7b0442035754.json"

client = bigquery.Client(project='vast-incline-169817')

query = "SELECT * FROM ChatBot_QA.OA_QA"

data_frame = pd.read_gbq(query, 'vast-incline-169817')

oa = data_frame.to_dict(orient='records')

oa = [
	{'id': 0,
     'questions': 'what are the factors affecting pain in osteoarthritis',
     'answers': "The perception of pain depends not only on the disease process and the brain's processing of pain messages, but also on cultural, gender, and psychological factors.",
     },
    {'id': 1,
     'questions': 'what are the causes of sudden low back pain',
     'answers': 'Cancer involving the spine',
     }
]


@app.route('/', methods=['GET'])
def home():
    return "<h1>osteoarthritis</h1><p>This site answers the questions on osteoarthritis.</p>"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(oa)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'questions' in request.args:
        questions = str(request.args['questions'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    some = []
    for book in oa:
        some.append(text_to_vector(book['questions']))
    scores = []
    for i in some:
        scores.append(get_cosine(i, text_to_vector(questions)))
    max_value = max(scores)
    if max_value > 0.60:
        max_index = scores.index(max_value)
        #if book['questions'] == questions:
        results.append(oa[max_index])
   
    

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

if __name__ == '__main__':


    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run()

