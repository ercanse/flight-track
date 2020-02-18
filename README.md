# flight-track
A Flask application for tracking flights close to a given location.
It uses data collected from [Flightradar24](https://www.flightradar24.com/).

The initial page shows a list of all flights within a radius of about 15 kilometers from this location.
Clicking on a flight then redirects to a page with more details about the flight.

## Configuration

To configure the application, create a `config.py` in the project root with the following content, 
specifying a custom latitude and longitude:
```python
location = {'latitude': 0.000000, 'longitude': 0.000000}
```

## Running
#### As a Flask app
```
pip install -r requirements.txt
export FLASK_APP=ui.py
python -m flask run
```

#### Using a Docker container
```
docker build -t flight-track:1.0.0 .
docker run -p 5000:5000 flight-track:1.0.0
```

Test using `curl localhost:5000/flights`.