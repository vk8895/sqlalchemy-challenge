# 1. Do your imports

import sqlalchemy
import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# 2. Setup Database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define Flask Routes

# 3a. Homepage
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    
    return (
    f"Aloha! Here is your Hawaii Vacation Plan Page!<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation</br>"
    f"/api/v1.0/station</br>"
    f"/api/v1.0/temperatures</br>"
    f"/api/v1.0/<start></br>"
    f"/api/v1.0/<start>/<end>"    
    )

# 3b. Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
	
	# Create session (link) from Python to the DB
	session = Session(engine)
	
	# Make session queries
	time_prcp = session.query(Measurement.date, Measurement.prcp).all()

	# Close session
	session.close()
	
	# Jsonify for display
	return jsonify(time_prcp)

# 3c. Stations
@app.route("/api/v1.0/station")
def station():
  
  	# Create session (link) from Python to the DB
	session = Session(engine)
	
	# Make session queries
	station = session.query(Measurement.station).distinct().all()
		
	# Close session
	session.close()
	
	# Jsonify for display
	return jsonify(station)

# 3d. Temperatures from most active station
@app.route("/api/v1.0/temperatures")
def temperatures():

  	# Create session (link) from Python to the DB
	session = Session(engine)
	
	# Make session queries
	temperatures = session.query(Measurement.date, Measurement.tobs).\
    	filter(Measurement.station == 'USC00519281').\
    	filter(Measurement.date >= '2016-08-23').\
    	filter(Measurement.date <= '2017-08-23').all()
		
	# Close session
	session.close()
	
	# Jsonify for display
	return jsonify(temperatures)

# 3e. Find min/max/avg temp for dates after start date (and between start/end date)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def startend(start=None, end=None):
	
	# Create session (link) from Python to the DB
	session = Session(engine)

	# Make session queries
	
	temp_list = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
	
	if not end:
		start = session.query(*temp_list).\
			filter(Measurement.date >= start).all() 
	
	# Jsonify for display
		return jsonify(start)	
		
	#else:
	
	startend = session.query(*temp_list).\
		filter(Measurement.date >= start).filter(Measurement.date <= end).all() 	
	
    # Jsonify for display
	return jsonify(startend)
	
	# Close session
	session.close()
	
if __name__ == "__main__":
    app.run(debug=True)



