# importing dependencies

from operator import and_
import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
session = Session(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/startdate/enddate"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a series of precipitations"""
    # Query all passengers
    results_prcp = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    #Create a dictionary with the date as key and prcp as the value
    precip = {date: prcp for date, prcp in results_prcp}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
# Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a series of stations"""
    # Query all stations
    results_station = session.query(Station.name, Station.station).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for name_st, code in results_station:
        station_dict = {}
        station_dict["station_name"] = name_st
        station_dict["code"] = code
        all_stations.append(station_dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
# Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a series of stations"""
    # Query all stations
    # to address the date a year from the last entry ( = 2016/08/23) and the station with the highest number, we refer back to the SQLAlchemy data
    tobs = session.query(Measurement.date, Measurement.tobs).\
           filter(and_(Measurement.date >= 2016/8/23).\
                       Measurement.station == "USC00519281")
    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_tobs = []
    for name_st, code in results_station:
        station_dict = {}
        station_dict["station_name"] = name_st
        station_dict["code"] = code
        all_stations.append(station_dict)
    return jsonify(all_stations)

"""""
@app.route("/api/v1.0/<start_date>")
def start_temp(start_date):
    TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    
    
    start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()
    return jsonify(start_temp)
"""

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return jsonify(list(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()))


if __name__ == "__main__":
    app.run(debug=True)
