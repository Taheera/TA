
import MySQLdb

def connection():
    # Edited out actual values
    conn = MySQLdb.connect(host="us-cdbr-iron-east-01.cleardb.net",
                           user="b88587cadf13d9",
                           passwd="heroku_891d0a5899fbdca",
                           db = "TA")
    c = conn.cursor()

    return c, conn

