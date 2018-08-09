
# coding: utf-8

# In[1]:


import flask
from flask import request, jsonify, make_response
import re, math
from collections import Counter
import json
import pandas as pd
from __future__ import print_function


# In[2]:


import urlparse
from urllib import urlencode
from urllib import urlopen 
from urllib2 import HTTPError,Request
import os


# In[3]:


import google.cloud
from google.cloud import bigquery


# In[4]:


app = flask.Flask(__name__)
app.config["DEBUG"] = False


# In[5]:


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


# In[6]:


def processRequest(req):
    #if req.get("queryResult").get("action") != "interest":
    if req.get("queryResult").get("action") != "osteo-info":
        return {}
    baseurl = "http://9b8e1d2d.ngrok.iohttp://59d20dae.ngrok.io/api/v1/resources/books?questions="
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


# In[7]:


@app.route('/test', methods=['GET'])
def test():
    return  "Hello there my friend !!"


# In[8]:


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


# In[9]:


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


# In[10]:


def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)


# In[11]:


import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/css116549.CSSCORP/Desktop/Project/Project/Google Project-7b0442035754.json"


# In[12]:


client = bigquery.Client(project='vast-incline-169817')


# In[13]:


query = "SELECT * FROM ChatBot_QA.OA_QA"


# In[14]:


data_frame = pd.read_gbq(query, 'vast-incline-169817')


# In[15]:


oa = data_frame.to_dict(orient='records')


# In[16]:


oa


# In[17]:


@app.route('/', methods=['GET'])
def home():
    return "<h1>osteoarthritis</h1><p>This site answers the questions on osteoarthritis.</p>"


# In[18]:


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(oa)


# In[19]:


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


# In[ ]:


if __name__ == '__main__':


    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run()

