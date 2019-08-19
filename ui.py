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


@app.route("/flight/<string:ads_hex>")
def flight(ads_hex):
    flight_info = get_flight_info(ads_hex)
    return render_template('flight.html', flight=flight_info)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
