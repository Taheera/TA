import flask
from flask import request, jsonify
import re, math
from collections import Counter
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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

#json_data=open('data.json').read()
#oa = json.loads(json_data)


oa = [
	{'id': 0,
     'questions': 'what are the factors affecting pain in osteoarthritis',
     'answers': "The perception of pain depends not only on the disease process and the brain's processing of pain messages, but also on cultural, gender, and psychological factors.",
     },
    {'id': 1,
     'questions': 'what are the causes of sudden low back pain',
     'answers': 'Cancer involving the spine.',
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


app.run()