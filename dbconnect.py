
# coding: utf-8

# In[5]:


import MySQLdb


# In[6]:


def connection():
    # Edited out actual values
    conn = MySQLdb.connect(host="127.0.0.1",
                           user="root",
                           passwd="Sep3@2018",
                           db = "TA")
    c = conn.cursor()

    return c, conn

