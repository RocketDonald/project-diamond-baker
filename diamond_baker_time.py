import math
from astral import LocationInfo
from astral.sun import sun, elevation
from datetime import timedelta, date
import pytz

# TODO - Change these values to calculate for a different observing location
OUR_LATTITUDE = 49.33100
OUR_LONGITUDE = -123.26207
OUR_ALTITUDE = 0 # Measured in meters
OUR_REGION = "CANADA"
OUR_TIMEZONE = "America/Vancouver"
OUR_YEAR = 2024
OUR_MONTH = 10
OUR_DAY = 26

# DO NOT CHANGE THESE VALUES UNLESS YOU WANT TO CALCULATE FOR A DIFFERENT LOCATION
MT_BAKER_HEIGHT = 3286
MT_BAKER_LATTITUDE = 48.776403
MT_BAKER_LONGITUDE = -121.819222

# Define ANSI escape codes for colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface using the Haversine formula.
    Parameters:
    lat1 (float): Latitude of the first point in degrees.
    lon1 (float): Longitude of the first point in degrees.
    lat2 (float): Latitude of the second point in degrees.
    lon2 (float): Longitude of the second point in degrees.
    Returns:
    float: Distance between the two points in kilometers.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in kilometers. Use 3956 for miles. Determines return value units.
    r = 6371
    
    # Calculate the result
    return c * r

def calculate_sunrise_and_altitude(location, custom_date, target_altitude):
    # Calculate sunrise time for the custom date
    s = sun(location.observer, date=custom_date)
    sunrise_time = s['sunrise']

    # Convert sunrise time to Vancouver timezone
    our_tz = pytz.timezone(OUR_TIMEZONE)
    sunrise_time_adjusted_timezone = sunrise_time.astimezone(our_tz)

    # Calculate the time when the sun reaches the target altitude
    time_interval = timedelta(minutes=1)
    current_time = sunrise_time_adjusted_timezone
    while True:
        current_altitude = elevation(location.observer, current_time)
        if current_altitude >= target_altitude:
            break
        current_time += time_interval
        
    # Format the times into Hour:Minute:Second
    sunrise_time_formatted = sunrise_time_adjusted_timezone.strftime('%H:%M:%S')
    target_time_formatted = current_time.strftime('%H:%M:%S')

    return sunrise_time_formatted, target_time_formatted, current_altitude

def calculate_altitude_angle(target_height, distance, observing_point_height):
    # Adjust the height by subtracting the observing point height
    adjusted_height = target_height - observing_point_height
    # Calculate the altitude angle in radians
    altitude_angle_radians = math.atan(adjusted_height / distance)
    # Convert the angle to degrees
    altitude_angle_degrees = math.degrees(altitude_angle_radians)
    return altitude_angle_degrees

if __name__ == "__main__":
    our_date = date(OUR_YEAR, OUR_MONTH, OUR_DAY)
    location = LocationInfo(region= OUR_REGION, latitude=OUR_LATTITUDE, longitude=OUR_LONGITUDE, timezone=OUR_TIMEZONE)
    distance = haversine(OUR_LATTITUDE, OUR_LONGITUDE, MT_BAKER_LATTITUDE, MT_BAKER_LONGITUDE)
    print(f"Distance between our location and Mt. Baker is {distance:.2f} km")
    print(f"Mt. Baker is {MT_BAKER_HEIGHT} meters tall")
    
    # Calculate the altitude angle of Mount Baker from the current location
    altitude_angle = calculate_altitude_angle(MT_BAKER_HEIGHT, distance * 1000, OUR_ALTITUDE)  # Convert distance to meters
    print(f"Altitude angle of Mount Baker from the current location is {altitude_angle:.2f} degrees")

    sunrise_time_vancouver, target_time, target_altitude = calculate_sunrise_and_altitude(location, our_date, altitude_angle)
    print(f"Sunrise time on {our_date} in Vancouver timezone is {sunrise_time_vancouver}")
    print(f"Time when the sun reaches the altiude angle {altitude_angle:.4f} degrees is {target_time}")
    print("===============================================\n")
    print(f"{Colors.BOLD}{Colors.OKCYAN}Time when the sun reaches the peak of Mount Baker from our observing location is {target_time}.{Colors.ENDC}")
    print("\n===============================================")
    
    
    """
    Possible observing locations and times:
    - 2024 October 16th - 7:51:38 AM - Latitude: 49.01631, Longitude: -123.04103
    - 2024 October 18th - 7:54:48 AM - Latitude: 49.03736, Longitude: -123.05168
    - 2024 October 26th - 8:07:43 AM - Latitude: 49.11949, Longitude: -123.09661
    - 2024 November 11th - 7:32:41 AM - Latitude: 49.33100, Longitude: -123.26207
    """