# Reference Section 10, Day 3, Module 10 for imports
from flask import Flask, jsonify

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Database setup
# Reference Section 10, Day 3, Module 10
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

session = Session(engine)


# Flask Routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the SQLAlchemy API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start><br/>"
        f"/api/v1.0/temp/<start>/<end><br/>" 
    )


# Precipitation path

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
  

    """Return a list of all precipitation data"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
#     all_precipitation = list(np.ravel(results))

#     return jsonify(all_precipitation)

# Create a dictionary from the row data and append to a list of all_passengers
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)


# Stations path

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB

    """Return a list of all Stations"""
    # Query all stations
    results = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Tobs path

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB

    """Return a list of all Dates and Temps from station USC00519281"""
    # Query all Temps
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.station == "USC00519281").order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

# Temp Start Date & Time Start Date/End Date Path
# With assistance from TA, we combined the two API's with a if statement

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def start_date_temps(start=None,end=None):
    if not end:

         """Fetch the start date whose start matches
           the path variable supplied by the user"""
        # Query all Temps
         results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    else:
         results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
       
    

    data_temps = list(np.ravel(results))

    return jsonify(data_temps)





if __name__ == "__main__":
    app.run(debug=True)
