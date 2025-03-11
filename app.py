from flask import Flask, render_template, request
import datetime
from astral import LocationInfo
from astral.sun import sun
import pytz
from datetime import timezone, timedelta
import os  # Add this import to access environment variables

app = Flask(__name__)

# List of cities (same as before)
cities = [
    {"name": "New York, NY", "tz": "America/New_York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Los Angeles, CA", "tz": "America/Los_Angeles", "lat": 34.0522, "lon": -118.2437},
    {"name": "Chicago, IL", "tz": "America/Chicago", "lat": 41.8781, "lon": -87.6298},
    {"name": "Houston, TX", "tz": "America/Chicago", "lat": 29.7604, "lon": -95.3698},
    {"name": "Phoenix, AZ", "tz": "America/Phoenix", "lat": 33.4484, "lon": -112.0740},
    {"name": "Philadelphia, PA", "tz": "America/New_York", "lat": 39.9526, "lon": -75.1652},
    {"name": "San Antonio, TX", "tz": "America/Chicago", "lat": 29.4241, "lon": -98.4936},
    {"name": "San Diego, CA", "tz": "America/Los_Angeles", "lat": 32.7157, "lon": -117.1611},
    {"name": "Dallas, TX", "tz": "America/Chicago", "lat": 32.7767, "lon": -96.7970},
    {"name": "San Jose, CA", "tz": "America/Los_Angeles", "lat": 37.3382, "lon": -121.8863},
    {"name": "Austin, TX", "tz": "America/Chicago", "lat": 30.2672, "lon": -97.7431},
    {"name": "Jacksonville, FL", "tz": "America/New_York", "lat": 30.3322, "lon": -81.6557},
    {"name": "Fort Worth, TX", "tz": "America/Chicago", "lat": 32.7555, "lon": -97.3308},
    {"name": "Columbus, OH", "tz": "America/New_York", "lat": 39.9612, "lon": -82.9988},
    {"name": "Charlotte, NC", "tz": "America/New_York", "lat": 35.2271, "lon": -80.8431},
    {"name": "San Francisco, CA", "tz": "America/Los_Angeles", "lat": 37.7749, "lon": -122.4194},
    {"name": "Indianapolis, IN", "tz": "America/Indiana/Indianapolis", "lat": 39.7684, "lon": -86.1581},
    {"name": "Seattle, WA", "tz": "America/Los_Angeles", "lat": 47.6062, "lon": -122.3321},
    {"name": "Denver, CO", "tz": "America/Denver", "lat": 39.7392, "lon": -104.9903},
    {"name": "Washington, DC", "tz": "America/New_York", "lat": 38.9072, "lon": -77.0369},
    {"name": "Boston, MA", "tz": "America/New_York", "lat": 42.3601, "lon": -71.0589},
    {"name": "El Paso, TX", "tz": "America/Denver", "lat": 31.7619, "lon": -106.4850},
    {"name": "Nashville, TN", "tz": "America/Chicago", "lat": 36.1627, "lon": -86.7816},
    {"name": "Detroit, MI", "tz": "America/Detroit", "lat": 42.3314, "lon": -83.0458},
    {"name": "Oklahoma City, OK", "tz": "America/Chicago", "lat": 35.4676, "lon": -97.5164},
    {"name": "Portland, OR", "tz": "America/Los_Angeles", "lat": 45.5051, "lon": -122.6750},
    {"name": "Las Vegas, NV", "tz": "America/Los_Angeles", "lat": 36.1699, "lon": -115.1398},
    {"name": "Memphis, TN", "tz": "America/Chicago", "lat": 35.1495, "lon": -90.0490},
    {"name": "Louisville, KY", "tz": "America/Kentucky/Louisville", "lat": 38.2527, "lon": -85.7585},
    {"name": "Baltimore, MD", "tz": "America/New_York", "lat": 39.2904, "lon": -76.6122},
    {"name": "Milwaukee, WI", "tz": "America/Chicago", "lat": 43.0389, "lon": -87.9065},
    {"name": "Albuquerque, NM", "tz": "America/Denver", "lat": 35.0844, "lon": -106.6504},
    {"name": "Tucson, AZ", "tz": "America/Phoenix", "lat": 32.2226, "lon": -110.9747},
    {"name": "Fresno, CA", "tz": "America/Los_Angeles", "lat": 36.7378, "lon": -119.7871},
    {"name": "Sacramento, CA", "tz": "America/Los_Angeles", "lat": 38.5816, "lon": -121.4944},
    {"name": "Mesa, AZ", "tz": "America/Phoenix", "lat": 33.4152, "lon": -111.8315},
    {"name": "Atlanta, GA", "tz": "America/New_York", "lat": 33.7490, "lon": -84.3880},
    {"name": "Kansas City, MO", "tz": "America/Chicago", "lat": 39.0997, "lon": -94.5786},
    {"name": "Colorado Springs, CO", "tz": "America/Denver", "lat": 38.8339, "lon": -104.8214},
    {"name": "Miami, FL", "tz": "America/New_York", "lat": 25.7617, "lon": -80.1918},
    {"name": "Raleigh, NC", "tz": "America/New_York", "lat": 35.7796, "lon": -78.6382},
    {"name": "Omaha, NE", "tz": "America/Chicago", "lat": 41.2565, "lon": -95.9345},
    {"name": "Long Beach, CA", "tz": "America/Los_Angeles", "lat": 33.7701, "lon": -118.1937},
    {"name": "Virginia Beach, VA", "tz": "America/New_York", "lat": 36.8529, "lon": -75.9780},
    {"name": "Oakland, CA", "tz": "America/Los_Angeles", "lat": 37.8044, "lon": -122.2711},
    {"name": "Minneapolis, MN", "tz": "America/Chicago", "lat": 44.9778, "lon": -93.2650},
    {"name": "Tulsa, OK", "tz": "America/Chicago", "lat": 36.1539, "lon": -95.9928},
    {"name": "Arlington, TX", "tz": "America/Chicago", "lat": 32.7357, "lon": -97.1081},
    {"name": "Tampa, FL", "tz": "America/New_York", "lat": 27.9506, "lon": -82.4572},
    {"name": "New Orleans, LA", "tz": "America/Chicago", "lat": 29.9511, "lon": -90.0715},
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['city']
        dst_config = request.form['dst']
        date_str = request.form['date']
        
        # Find the selected city
        selected_city = next((city for city in cities if city['name'] == city_name), None)
        if not selected_city:
            return "City not found", 400
        
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD.", 400
        
        tz = pytz.timezone(selected_city["tz"])
        
        # Calculate standard offset
        year = date.year
        non_dst_dt = tz.localize(datetime.datetime(year, 1, 1), is_dst=False)
        std_offset = non_dst_dt.utcoffset().total_seconds() / 3600
        
        # Compute solar times in UTC
        location = LocationInfo(selected_city["name"], "USA", "UTC", selected_city["lat"], selected_city["lon"])
        s = sun(location.observer, date=date, tzinfo=pytz.UTC)
        sunrise_utc = s["sunrise"]
        sunset_utc = s["sunset"]
        solar_noon_utc = s["noon"]
        
        # Determine target time zone based on DST configuration
        if dst_config == "Current DST":
            target_tz = tz
        elif dst_config == "Never DST":
            target_tz = timezone(timedelta(hours=std_offset))
        elif dst_config == "Always DST":
            target_tz = timezone(timedelta(hours=std_offset + 1))
        
        # Convert UTC times to local time
        sunrise_local = sunrise_utc.astimezone(target_tz).strftime('%H:%M')
        sunset_local = sunset_utc.astimezone(target_tz).strftime('%H:%M')
        solar_noon_local = solar_noon_utc.astimezone(target_tz).strftime('%H:%M')
        
        return render_template('index.html', cities=cities, selected_city=city_name, dst_config=dst_config, date=date_str, sunrise=sunrise_local, sunset=sunset_local, solar_noon=solar_noon_local)
    
    return render_template('index.html', cities=cities)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Use PORT environment variable, default to 5000 if not set
    app.run(host='0.0.0.0', port=port, debug=False)  # Bind to 0.0.0.0 and use the specified port
