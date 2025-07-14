import requests
from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime
import airportsdata
import plotly.graph_objs as go
import plotly
import json
import os

app = Flask(__name__)

def fetch_opensky_data():
    """
    Fetches flight data from the OpenSky Network API for the last hour.
    Returns a list of flight dictionaries.
    """
    now = int(datetime.utcnow().timestamp())
    one_hour_ago = now - 3600
    url = f"https://opensky-network.org/api/flights/all?begin={one_hour_ago}&end={now}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"API Error: {e}")
    return []

def get_airport_name(icao, airports):
    """
    Returns the full airport name with ICAO code, or just the code if not found.
    """
    info = airports.get(icao)
    if info:
        return f"{info['name']} ({icao})"
    return icao

@app.route('/', methods=['GET', 'POST'])
def index():
    airports = airportsdata.load()
    flights = fetch_opensky_data()
    df = pd.DataFrame(flights)

    # Initialize variables for template context
    popular_routes_dict = {}
    has_data = False
    chartJSON = None
    origins_named = {}
    destinations_named = {}
    total_flights = 0

    if not df.empty:
        # Data cleaning: remove rows with missing or identical airports
        df = df.dropna(subset=['estDepartureAirport', 'estArrivalAirport'])
        df = df[df['estDepartureAirport'] != df['estArrivalAirport']]

        # Calculate popular origins/destinations
        popular_origins = df['estDepartureAirport'].value_counts().head(5)
        popular_destinations = df['estArrivalAirport'].value_counts().head(5)

        # Map ICAO codes to names for display and dropdowns
        origins_named = {icao: get_airport_name(icao, airports) for icao in popular_origins.index}
        destinations_named = {icao: get_airport_name(icao, airports) for icao in popular_destinations.index}

        # Handle filter from form
        selected_origin = request.form.get('origin_filter')
        if selected_origin and selected_origin != "All":
            # Reverse map: find ICAO code for selected name
            for icao, name in origins_named.items():
                if name == selected_origin:
                    df = df[df['estDepartureAirport'] == icao]
                    break

        if not df.empty:
            # Create readable route strings
            df['route'] = df['estDepartureAirport'].apply(lambda x: get_airport_name(x, airports)) + " → " + df['estArrivalAirport'].apply(lambda x: get_airport_name(x, airports))
            popular_routes = df['route'].value_counts().head(5)
            popular_routes_dict = popular_routes.to_dict()
            has_data = not popular_routes.empty
            total_flights = len(df)

            # Horizontal bar chart for best readability
            if has_data:
                routes = list(popular_routes_dict.keys())
                counts = list(popular_routes_dict.values())
                bar = go.Bar(
                    x=counts,
                    y=routes,
                    orientation='h',
                    text=routes,
                    hoverinfo='text+x'
                )
                layout = go.Layout(
                    title='Popular Flight Routes (Last Hour)',
                    xaxis=dict(title='Number of Flights'),
                    yaxis=dict(title='Route', automargin=True),
                    margin=dict(l=200, r=40, t=60, b=40),
                    height=450
                )
                fig = go.Figure(data=[bar], layout=layout)
                chartJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        'index.html',
        popular_routes=popular_routes_dict,
        has_data=has_data,
        chartJSON=chartJSON,
        popular_origins=origins_named,
        popular_destinations=destinations_named,
        total_flights=total_flights
    )




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=port, debug=True)

