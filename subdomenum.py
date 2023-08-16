
import requests
import socket
import whois
import json
from pymongo import MongoClient
def get_subdomains(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    response = requests.get(url)
    subdomains = set()
    if response.ok:
        data = response.json()
        for entry in data:
            subdomains.add(entry['name_value'])
    return subdomains

def get_ip_addresses(domain):
    try:
        ips = socket.gethostbyname_ex(domain)
        return ips[2]
    except socket.gaierror:
        return []

def get_whois_data(domain):
    return whois.whois(domain)

if __name__ == "__main__":
    domain_to_check = input("Enter the domain you want to investigate: ")

    subdomains = get_subdomains(domain_to_check)
    print(f"Subdomains for {domain_to_check}:")
    print(subdomains)

    ip_addresses = get_ip_addresses(domain_to_check)
    print(f"IP addresses for {domain_to_check}:")
    print(ip_addresses)

    whois_data = get_whois_data(domain_to_check)
    if whois_data:
        whois_data['creation_date'] =str(whois_data['creation_date'])
        whois_data['expiration_date'] =str(whois_data['expiration_date'])
        whois_data['updated_date'] =str(whois_data['updated_date'])



        print(f"WHOIS data for {domain_to_check}:")
        print(whois_data)
    else:
        print("Failed to retrieve WHOIS data.")

    # Collect all the data into a single dictionary
    all_data = {
        "domain": domain_to_check,
        "subdomains": list(subdomains),
        "ip_addresses": ip_addresses,
        "whois_data": whois_data
    }

    # Save all information to a JSON file
    with open(f"{domain_to_check}_all_data.json", "w") as f:
        json.dump(all_data, f, indent=2)
    print("All information saved to JSON file.")

    # MongoDB Integration
    try:
        # MongoDB connection Paremeters
        db_user = "root"
        db_password ="Sf409xqyNL3Eyue"
        db_host = "10.10.10.31"
        db_port = "27017"
        db_name = "threatmap_db"

        # MongoDB connection String
        connection_string = f"mongodb://root:Sf409xqyNL3Eyue@10.10.10.31:27017/?authMechanism=DEFAULT"

        # connect to MongoDB
        client = MongoClient(connection_string)
        db = client[db_name]

        # collection    name
        collection_name = 'domain_data'

        # Insert the data into the MongoDB collection
        collection=db[ collection_name]
        collection.insert_one(all_data)  
        print("Data sent to MongoDB.")
    except Exception as e:
        print(f"Failed to send data to MongoDB: {e}")