from pyproj import Proj, transform

# Define the projections
epsg3857 = Proj(init='epsg:3857')  # Web Mercator
wgs84 = Proj(init='epsg:4326')     # WGS84 GPS coordinates

# Example coordinates in Web Mercator
x = 252421
y = 6247170

# Perform the transformation
lon, lat = transform(epsg3857, wgs84, x, y)

print(f"GPS Coordinates (WGS84): Latitude {lat}, Longitude {lon}")

