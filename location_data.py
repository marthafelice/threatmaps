
import pymongo
import requests

    
def get_location_info(organization_name, api_key):
    # Google Places API endpoint for place search
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

    # Set up parameters for the request
    params = {
        "input": organization_name,
        "inputtype": "textquery",
        "fields": "geometry,formatted_address",
        "key": api_key,
    }
    
   
    try:
      
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])

            if candidates:
                for i, candidate in enumerate(candidates):
                    formatted_address = candidate.get("formatted_address", "Location not found")
                    geometry = candidate.get("geometry", {})
                    location = geometry.get("location", {})
                    latitude = location.get("lat", "Latitude not found")
                    longitude = location.get("lng", "Longitude not found")
                    location_data = {
                    "organization_name": organization_name,
                    "address": formatted_address,
                    "latitude": latitude,
                    "longitude": longitude
                   }
                    return location_data
            else:
                print(f"No location information found for {organization_name}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")    
        
        

if __name__ == "__main__":    
    myclient = pymongo.MongoClient("mongodb://root:Sf409xqyNL3Eyue@10.10.10.31:27017/?authMechanism=DEFAULT")
    mydb = myclient["the_eagle"]
    mycol = mydb["Domains"]
    api_key = "AIzaSyDvPCUNgMDugc5L0PkZ93nQWZADegqvwDM"
    
    # unknown_organisation = ['Domains By Proxy, LLC', 'REDACTED FOR PRIVACY', 
    #                         'Contact Privacy Inc. Customer  0155877898', 'Private by Design, LLC'
    #                         'Privacy service provided by Withheld for Privacy ehf']
    
    for document in mycol.find({'who_is_data':{'$exists':True,'$ne':[]}}, {"_id": 1, "who_is_data.org":1}):
        organization_name = document["who_is_data"]["org"]  
        resolve_location = get_location_info(organization_name, api_key)
        print(resolve_location)
        
        # mycol.update_one({ '_id': document["_id"]},{"$set":{'organisation_location' : resolve_organisation_name}})



   



# if __name__ == "__main__":
#     
#     organization_name = input("Enter the organization name: ")
    
#     get_location_info(organization_name, api_key)

