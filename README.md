# Airline Booking Market Demand Web App

## Overview

This web application provides real-time insights into airline booking market demand, designed specifically for hostel managers and business analysts across multiple cities in Australia. The app fetches live flight data, processes it to identify popular routes, origins, and destinations, and displays these insights through an intuitive, user-friendly interface.

## Features

- **Real-time flight data** sourced from the OpenSky Network API.
- Identification of **popular flight routes**, **origin airports**, and **destination airports**.
- Interactive **bar charts** for visualizing flight route demand.
- **Filter flights by origin airport** to customize insights.
- Responsive and clean UI built with **Bootstrap**.
- Robust error handling and fallback mechanisms to ensure reliability.

## Setup Instructions

1. **Clone the repository:**
git clone https://github.com/yourusername/airline-demand-app.git
cd airline-demand-app

text

2. **Create and activate a virtual environment:**

  python -m venv venv
  venv\Scripts\activate
  


3. **Install dependencies:**
pip install -r requirements.txt



4. **Run the application:**
python app.py



5. **Open your browser and navigate to:**
http://127.0.0.1:5000



## Usage

- Use the dropdown menu to filter flights by origin airport or view all flights.
- Review the popular flight routes and airports displayed.
- Analyze the interactive bar chart to understand flight demand trends.
- Use insights to inform hostel marketing strategies and partnership decisions.

## Deployment

For deploying this app on cloud platforms like Heroku or Render, refer to the `DEPLOYMENT.md` file included in this repository for detailed instructions.

## Dependencies

- Flask
- Pandas
- Requests
- Plotly
- airportsdata

## Project Structure

airline-demand-app/
├── app.py
├── requirements.txt
├── README.md
├── DEPLOYMENT.md
└── templates/
└── index.html


## Acknowledgments

- Flight data provided by the [OpenSky Network API](https://opensky-network.org/apidoc/rest.html).
- Airport data courtesy of the [airportsdata Python package](https://pypi.org/project/airportsdata/).
- Visualization powered by [Plotly](https://plotly.com/python/).
- UI styled with [Bootstrap](https://getbootstrap.com/).

## License

This project is licensed under the MIT License.

---

Thank you for reviewing this project! I look forward to the opportunity to contribute my skills and grow with your team.