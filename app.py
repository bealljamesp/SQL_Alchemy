import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f'/api/v1.0/start/end'
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()

    # Convert list of tuples into normal list
    prec_list = list(np.ravel(results)) 

    # Return the JSON representation of your dictionary.
    return jsonify(prec_list)
    

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.station).all()
    
    session.close()

    # Convert list of tuples into normal list
    stat_list = list(np.ravel(results)) 

    # Return a JSON list of stations from the dataset.
    return jsonify(stat_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').all()
    
    session.close()

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    tobs_list = list(np.ravel(results)) 
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.station).filter(Measurement.date >= start).all()
    
    st_tbs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    print(st_tbs)
    session.close()

    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the max temperature for a given start.
    start_list = list(np.ravel(st_tbs))
    return jsonify(start_list)

    # When given the start only, calculate TMIN, TAVG, and 
    # TMAX for all dates greater than and equal to the start date.


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    sted_tbs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the max temperature for a given start-end range.
    range_list = list(np.ravel(sted_tbs)) 
    return jsonify(range_list)


if __name__ == '__main__':
    app.run(debug=True)
