# import dns.resolver
# import sys

# record_types=['A','AAAA','NS','CNAME','MX','PTR','SOA','TXT']
# try:
#     domain=sys.argv[1]
# except IndexError:
#     print('Syntax Error- python demodns.py <domainname>')
#     quit()    
# for records in record_types:
#     try:
#         answer =dns.resolver.resolve(domain,records)
#         print(f'{records} Records')
#         print('-'*50)
#         for ipval in answer:
#             print (ipval.to_text() + '\n')
#     except dns.resolver.NoAnswer:
#         pass
#     except dns.resolver.NXDOMAIN:
#         print(f'{domain} does not exist')
#     except KeyboardInterrupt:
#         print('Goodbye...')
#         quit()
# import whois
# print(whois.whois("test.com"))
# import whois
# print(whois.whois("test.com"))


import requests
import socket
import whois
import json
import pandas as pd
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

def process_and_save_data(name, domain_to_check, category, subcategory):
    subdomains = get_subdomains(domain_to_check)
    print(f"Subdomains for {domain_to_check}:")
    print(subdomains)

    ip_addresses = get_ip_addresses(domain_to_check)
    print(f"IP addresses for {domain_to_check}:")
    print(ip_addresses)

    whois_data = get_whois_data(domain_to_check)
    if whois_data:
        # Convert datetime objects to strings before adding them to the dictionary
        whois_data['creation_date'] = str(whois_data['creation_date'])
        whois_data['expiration_date'] = str(whois_data['expiration_date'])
        whois_data['updated_date'] = str(whois_data['updated_date'])

        print(f"WHOIS data for {domain_to_check}:")
        print(whois_data)
    else:
        print("Failed to retrieve WHOIS data.")

    # Collect all the data into a single dictionary
    all_data = {
        "name": name,
        "domain": domain_to_check,
        "category": category,
        "subcategory": subcategory,
        "subdomains": list(subdomains),
        "ip_addresses": ip_addresses,
        "whois_data": whois_data
    }

 

    # MongoDB Integration (if desired)
    try:
        # MongoDB Connection Parameters
        db_user = "xxx"
        db_password = "xxx"
        db_host = "xxx" 
        db_port = "xxxx"
        db_name = "xxx"  

        # MongoDB Connection String
        connection_string = f"mongodb://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

        # Connect to MongoDB
        client = MongoClient(connection_string)
        db = client[db_name]

        # Specify the collection name where you want to insert the data
        collection_name = "domain_data"

        # Insert the data into the MongoDB collection
        collection = db[collection_name]
        collection.insert_one(all_data)
        print("Data sent to MongoDB.")
    except Exception as e:
        print(f"Failed to send data to MongoDB: {e}")

if __name__ == "__main__":
    excel_file = input("Enter the path to the Excel file with domain data: ")
    
    try:
        # Read domain data from Excel sheet
        df = pd.read_excel(excel_file)
        
        for index, row in df.iterrows():
            domain = row['Domain']
            category = row['Sector']


            process_and_save_data(domain, category)
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        
        
      
