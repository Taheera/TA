
#from dbconnect import connection
import flask
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sep3@2018@localhost/TA'
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def home():
    try:
        #c, conn = connection()
        query = text("SELECT * from employee")
        #c.execute(query)
        #data = c.fetchall()
        #conn.close()
        #return data
        data = db.engine.execute(query)
        return render_template("dashboard.html", data=data)
    except Exception as e:
        return (str(e))
    
app.run()

