
from dbconnect import connection
import flask
from flask import Flask, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = False

@app.route('/', methods=['GET'])
def home():
    try:
        c, conn = connection()
        query = ("SELECT * from employee")
        c.execute(query)
        data = c.fetchall()
        conn.close()
        #return data
        return render_template("dashboard.html", data=data)
    except Exception as e:
        return (str(e))
    
app.run()

