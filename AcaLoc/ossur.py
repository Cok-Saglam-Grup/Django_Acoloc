import openrouteservice as ors
import folium

ors_key = "5b3ce3597851110001cf624868767a25d6ad4aafb8da4295bbd1cb19"

# performs requests to the ORS API services
# client will be used in all examples
client = ors.Client(key=ors_key)


# coordinates from Nashville, TN (-86.781247, 36.163532) to Miami, FL (-80.191850, 25.771645)
# order for coordinates is [lon, lat]
coordinates = [[32.73553031509989,39.870198227874766], [32.7402689103697,39.86717478717732]]

# directions
route = client.directions(coordinates=coordinates,
                          profile='foot-walking',
                          format='geojson')

# map
map_directions = folium.Map(location=[39.86804387298904, 32.733501664850834], zoom_start=5)

# add geojson to map
folium.GeoJson(route, name='route').add_to(map_directions)

# add layer control to map (allows layer to be turned on or off)
folium.LayerControl().add_to(map_directions)

# display map
map_directions.save("templates/AcaLoc/showmap.html")