import requests
import urllib.parse
route_url = "https://graphhopper.com/api/1/route?"
def geocoding (location, key):
    while location == "":
        location = input("Ingrese la ciudad nuevamente: ")

    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200:
        json_data = requests.get(url).json()
        lat=(json_data["hits"][0]["point"]["lat"])
        lng=(json_data["hits"][0]["point"]["lng"])
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""
        
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""
        
        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        
        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data["message"])

    return json_status,lat,lng,new_loc


while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehículos disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile=["car", "bike", "foot"]
    vehicle = input("Ingrese una de las opciones: ")
    if vehicle == "s":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else: 
        vehicle = "car"
        print("No se ingresó un vehículo válido. Usando el auto.")
    key = "56fc2a27-390f-4ba9-9e23-09dc0a97b80e"
    loc1 = input("Ingrese ciudad de origen: ")
    if loc1 == "s":
        break
    orig = geocoding(loc1, key)
    loc2 = input("Ingrese ciudad de destino: ")
    if loc2 == "s":
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key, "Medio de transporte: ":vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
    print("=================================================")
    print("Información desde " + orig[3] + " a " + dest[3] + " en" + vehicle)
    print("=================================================")

    if paths_status == 200:
        miles = (paths_data["paths"][0]["distance"])/1000/1.61
        km = (paths_data["paths"][0]["distance"])/1000
        sec = int(paths_data["paths"][0]["time"]/1000%60)
        min = int(paths_data["paths"][0]["time"]/1000/60%60)
        hr = int(paths_data["paths"][0]["time"]/1000/60/60)

        print("Distancia Recorrida: {0:.1f} millas / {1:.1f} km".format(miles, km))
        print("Duración del Viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
        for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} millas )".format(path, distance/1000, distance/1000/1.61))
        print("=============================================")
    else:
            print("Error message: " + paths_data["message"])
            print("*************************************************")





