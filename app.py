

# Import Dependencies
import datetime as dt
import numpy as np
import pandas as pdimport
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, MetaData, Table, Column
from flask import Flask, jsonify
import config #import user, password

# Create engine, automap and session
# db Setup
engine = create_engine(f'postgres://{config.user}:{config.password}@ec2-52-22-216-69.compute-1.amazonaws.com:5432/d5qr295as59lsj')
base = automap_base()
base.prepare(engine, reflect=True)
session = Session(engine)


fire_table = base.classes.fires_2013_2017


# In[7]:


# flask setup
app = Flask(__name__)


# In[ ]:


#############################################
# /api/v1.0/interactive_pie
#############################################

           
@app.route("/")
def welcome():
    return("Available Routes:<br/> /api/v1.0/interactive_pie/<fire_cause>/<st>/<year>")

@app.route("/api/v1.0/interactive_pie/<st>/<year>")
def interactive_pie(st, year):
    session = Session(engine)  
    pie_results = session.query(fire_table.st, fire_table.year,fire_table.month, fire_table.latitude1, fire_table.longitude1,                                fire_table.cause1, fire_table.cause2,fire_table.cause3, fire_table.cause4)    .filter(fire_table.st == st)    .filter(fire_table.year == year).all()
        #.filter(fire_table.cause1 == cause1)\
    #.filter(fire_table.cause2 == cause2)\
    
    session.close()
    
    pie_string = []
    for st, year, month, latitude1, longitude1, cause1, cause2, cause3, cause4 in pie_results:
        pie_data_dict = {}
        pie_data_dict["st"] = st
        pie_data_dict["year"] = year
        pie_data_dict["month"] = month
        pie_data_dict["latitude"] = latitude1
        pie_data_dict["longitude"] = longitude1    
        pie_data_dict["cause1"] = cause1
        pie_data_dict["cause2"] = cause2
        pie_data_dict["cause3"] = cause3
        pie_data_dict["cause4"] = cause4

        pie_string.append(pie_data_dict)
    return jsonify(pie_string)

# if __name__ == '__main__':
app.run(debug=False)


# In[ ]:




