from flask import Flask, render_template

from flight_radar.flight_radar import process, get_flight_info

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/flights")
def flights():
    flights_info = process()
    return render_template('flights.html', flights=flights_info)


@app.route("/flight/<string:reference>")
def flight(reference):
    flight_info = get_flight_info(reference)
    return render_template('flight.html', flight=flight_info)
