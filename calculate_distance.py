import pandas as pd

zone_data = pd.read_csv('data/taxi+_zone_lookup.csv')
zone_df = pd.DataFrame(zone_data)
zone_df = zone_df.dropna()

def fetch_zone(location_id):
    location_info = zone_df[zone_df["LocationID"] == location_id]
    if not location_info.empty:
        borough = location_info.iloc[0]["Borough"]
        zone = location_info.iloc[0]["Zone"]
        service_zone = location_info.iloc[0]["service_zone"]
        #return {"Borough": borough, "Zone": zone, "Service Zone": service_zone}
        return ', '.join([zone, borough])
    else:
        return None

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
count = 0
def get_coordinates_by_name(location_name):
    geolocator = Nominatim(user_agent="my_geocoder", timeout=10)
    location = geolocator.geocode(location_name)
    
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return 0,0

def calculate_distance(lat1, lon1, lat2, lon2):
    location1 = (lat1, lon1)
    location2 = (lat2, lon2)
    distance = geodesic(location1, location2).kilometers
    return distance

taxi_data = pd.read_csv('data/green_tripdata_2023-01.csv')
dist = []
diff_dist = []
for index, row in taxi_data.iterrows():
   zonePU = fetch_zone(row['PULocationID'])
   zoneDO = fetch_zone(row['DOLocationID'])
   latPU, lonPU = get_coordinates_by_name(zonePU)
   latDO, lonDO = get_coordinates_by_name(zoneDO)
   if (latPU==0 and lonPU==0) or (latDO==0 and lonDO==0):
        count = count + 1
   distance = calculate_distance(latPU, lonPU, latDO, lonDO)*0.621371
   dist.append(distance)
   diff = distance - row['trip_distance']
   diff_dist.append(diff)
taxi_data['distance']=dist
taxi_data['difference_distance']=diff_dist
print(taxi_data)
print("#############")
print(count)