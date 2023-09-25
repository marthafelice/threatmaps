# import pymongo
# import re

# try:
#     # Connect to your MongoDB server
#     client = pymongo.MongoClient("mongodb://root:Sf409xqyNL3Eyue@10.10.10.31:27017/?authMechanism=DEFAULT")
#     db = client["ifortify_threat_intelligence"]
#     collection = db['co_ug_domains']

#     # Initialize a list to store valid .co.ug domains
#     co_ug_domains = []
    
#     # Define a regular expression pattern to match domains that begin with numbers or contain asterisks
#     invalid_domain_pattern = r"^\d|[*]"

#     # Query the MongoDB collection
#     cursor = collection.find({})

#     for document in cursor:
#         # Extract the domain name from the "subject" key in the "cert" block
#         cert_subject = document.get("ssl", {}).get("cert", {}).get("subject", {})
#         domain_name_cert = cert_subject.get("CN", "")  # CN from "cert" block
        

#         # Extract .co.ug domains from the "domains" block
#         domains = document.get("domains", [])

#         # Check if the domain name from the "cert" block ends with ".co.ug" and is valid
#         if (
#             domain_name_cert.lower().endswith(".co.ug")
#             and not re.search(invalid_domain_pattern, domain_name_cert)
#             and domain_name_cert not in co_ug_domains
#         ):
#             co_ug_domains.append(domain_name_cert)

#         # Check .co.ug domains in the "domains" block and add valid ones to the list
#         for domain in domains:
#             if (
#                 domain.lower().endswith(".co.ug")
#                 and not re.search(invalid_domain_pattern, domain)
#                 and domain not in co_ug_domains
#             ):
#                 co_ug_domains.append(domain)

#     # Close the MongoDB connection
#     client.close()
    


#     # Print the collected valid .co.ug domains
#     for domain in co_ug_domains:
#        print(f"Domain Name: {domain}")


# except Exception as e:
#     print(f"An error occurred: {str(e)}")




# import pymongo
# import re

# try:
#     # Connect to your MongoDB server
#     client = pymongo.MongoClient("mongodb://root:Sf409xqyNL3Eyue@10.10.10.31:27017/?authMechanism=DEFAULT")
#     db = client["ifortify_threat_intelligence"]

#     # Initialize a list to store domains and IP addresses
#     ug_domains = []

#     # Define a regular expression pattern to match unwanted domains
#     invalid_domain_pattern = r"^\d|[*]"

#     # Helper function to process and filter domains based on the extension
#     def process_domains(collection, extension, domain_list):
#         cursor = collection.find({})
#         for document in cursor:
#             # Extract the domain name from the "subject" key in the "cert" block
#             cert_subject = document.get("ssl", {}).get("cert", {}).get("subject", {})
#             domain_name_cert = cert_subject.get("CN", "")  # CN from "cert" block
            
#             # Extract .co.ug, .go.ug, .or.ug, .ac.ug domains from the "domains" block
#             domains = document.get("domains", [])
        
#             if (
#                 domain_name_cert.lower().endswith(extension)
#                 and not re.search(invalid_domain_pattern, domain_name_cert)
#                 and domain_name_cert not in domain_list
#             ):
#                 # Extract the IP address from the "ip_str" block
#                 ip_address = document.get("ip_str", "")
#                 domain_list.append({"domain": domain_name_cert, "ip_address": ip_address})
                
#             # Check .co.ug domains in the "domains" block and add valid ones to the list
#             for domain in domains:
#                 if (
#                     domain.lower().endswith(extension)
#                     and not re.search(invalid_domain_pattern, domain)
#                     and domain not in domain_list
#                 ):
#                     # Extract the IP address from the "ip_str" block
#                     ip_address = document.get("ip_str", "")
#                     domain_list.append({"domain": domain, "ip_address": ip_address})

#     # Process .ac.ug domains
#     ac_ug_collection = db['ac_ug_domains']
#     process_domains(ac_ug_collection, ".ac.ug", ug_domains)

#     # Process .go.ug domains
#     go_ug_collection = db['go_ug_domains']
#     process_domains(go_ug_collection, ".go.ug", ug_domains)

#     # Process .or.ug domains
#     or_ug_collection = db['or_ug_domains']
#     process_domains(or_ug_collection, ".or.ug", ug_domains)
    
#     # Process .co.ug domains
#     co_ug_collection = db['co_ug_domains']
#     process_domains(co_ug_collection, ".co.ug", ug_domains)

#     # Print the combined list of .ug domains and IP addresses
#     for item in ug_domains:
#         print(f"Domain Name: {item['domain']}")
#         print(f"IP Address: {item['ip_address']}")

#     # Close the MongoDB connection
#     client.close()

# except Exception as e:
#     print(f"An error occurred: {str(e)}")

import pymongo
import re

try:
    # Connect to your MongoDB server
    client = pymongo.MongoClient("mongodb://root:Sf409xqyNL3Eyue@10.10.10.31:27017/?authMechanism=DEFAULT")
    db = client["ifortify_threat_intelligence"]

    # Initialize a dictionary to store unique domains and IP addresses
    ug_domains_ips = {}

    # Define a regular expression pattern to match unwanted domains
    invalid_domain_pattern = r"^\d|[*]"

    # Helper function to process and filter domains based on the extension
    def process_domains(collection, extension, domain_dict):
        cursor = collection.find({})
        for document in cursor:
            # Extract the domain name from the "subject" key in the "cert" block
            cert_subject = document.get("ssl", {}).get("cert", {}).get("subject", {})
            domain_name_cert = cert_subject.get("CN", "")  # CN from "cert" block
            
            # Extract .co.ug, .go.ug, .or.ug, .ac.ug domains from the "domains" block
            domains = document.get("domains", [])
        
            if (
                domain_name_cert.lower().endswith(extension)
                and not re.search(invalid_domain_pattern, domain_name_cert)
            ):
                # Extract the IP address from the "ip_str" block
                ip_address = document.get("ip_str", "")
                domain_dict[domain_name_cert] = ip_address
                
            # Check .co.ug domains in the "domains" block and add valid ones to the dictionary
            for domain in domains:
                if (
                    domain.lower().endswith(extension)
                    and not re.search(invalid_domain_pattern, domain)
                ):
                    # Extract the IP address from the "ip_str" block
                    ip_address = document.get("ip_str", "")
                    domain_dict[domain] = ip_address

    # Process .ac.ug domains
    ac_ug_collection = db['ac_ug_domains']
    process_domains(ac_ug_collection, ".ac.ug", ug_domains_ips)

    # Process .go.ug domains
    go_ug_collection = db['go_ug_domains']
    process_domains(go_ug_collection, ".go.ug", ug_domains_ips)

    # Process .or.ug domains
    or_ug_collection = db['or_ug_domains']
    process_domains(or_ug_collection, ".or.ug", ug_domains_ips)
    
    # Process .co.ug domains
    co_ug_collection = db['co_ug_domains']
    process_domains(co_ug_collection, ".co.ug", ug_domains_ips)

    # Insert the unique domain and IP address pairs into the "uganda_domains_ips" collection
    uganda_domains_ips_collection = db['uganda_domains_ips']
    for domain, ip_address in ug_domains_ips.items():
        uganda_domains_ips_collection.insert_one({"domain": domain, "ip_address": ip_address})

    # Close the MongoDB connection
    client.close()

except Exception as e:
    print(f"An error occurred: {str(e)}")
