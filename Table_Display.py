
#from dbconnect import connection
import flask
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b5e0ef8d514bf6:e0169a44@us-cdbr-iron-east-01.cleardb.net/heroku_517a14a1fceab5e'
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
    
if __name__ == '__main__':


    #port = int(os.getenv('PORT', 5000))
    port = int(os.environ.get("PORT", 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')

