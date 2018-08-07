from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


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
    baseurl = "https://4a1c508d.ngrok.io/api/v1/resources/books?questions="
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



if __name__ == '__main__':


    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
