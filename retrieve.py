from pymongo import MongoClient
import json
import pandas as pd


# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb://root:Sf409xqyNL3Eyue@10.10.10.31:27017/?authMechanism=DEFAULT')
filter={}
vulns_collection = client['ifortify_threat_intelligence_copy']['vulnerabilities']
domains_collection = client['ifortify_threat_intelligence_copy']['domains']
# vulns_ips = client['ifortify_threat_intelligence_copy']['vulnerabilities'].find({},{"_id": 0, "ip":1,"vulnerabilities":1})
domains_ip = client['ifortify_threat_intelligence_copy']['domains']
co_ug_collection =  client['ifortify_threat_intelligence_copy']['co_ug_domains']
ac_ug_collection =  client['ifortify_threat_intelligence_copy']['ac_ug_domains']
go_ug_collection =  client['ifortify_threat_intelligence_copy']['go_ug_domains']
or_ug_collection =  client['ifortify_threat_intelligence_copy']['or_ug_domains']



counter = 0

def combine_collections():
    for domain_ip in domains_collection.find({},{"_id": 1, "ip_address":1,"domain":1}):
              
        ip = domain_ip["ip_address"]
        domain_name = domain_ip["domain"]
        vulns_ips = vulns_collection.find_one({"ip" : ip},{"vulnerabilities":1})
        if vulns_ips: 
            print("Found IP "+ ip)
            print("For Domain Name "+ domain_name)
            print("adding vulnerablities")
            print()
            domains_collection.update_one({ '_id': domain_ip["_id"]},{"$set":{"vulnerabilities" : vulns_ips["vulnerabilities"]}})
          
            
# combine_collections()        

def add_missing_domains(collection , ends_with):
    for ughostnames in collection.find({},{"_id": 0, "domains":1,"ip_str":1,"location.country_name":1,"isp":1}):
        ugdomains = ughostnames["domains"]
        ip_address = ughostnames["ip_str"]
        country_of_hosting = ughostnames["location"]["country_name"]
        isp = ughostnames["isp"]
        for ugdomain in ugdomains:
        
            if str(ugdomain).endswith(ends_with):
                domain_domains = domains_collection.find_one({"domain": ugdomain})
                if domain_domains == None:
                    print("This domain Doesn't Exit")
                    print(ugdomain)
                    print("Inserting")
                    domains_collection.insert_one({"domain" : ugdomain, "ports": None, "ip_address": ip_address, "country_of_hosting":country_of_hosting, "isp":isp})
                # else:
                #     print("This Exists "+ ugdomain)
                    



def test():
    
    results =list(domains_collection.aggregate(
        [
            {
                "$match": {
                    
                    "ip_address": { "$exists":False } 
                    
                }
           
            }
        ]
    ))
    
    
    print(len(results))
    for result in results:
        print(result)

# test()


# add_missing_domains(ac_ug_collection, "ac.ug")
# add_missing_domains(go_ug_collection, "go.ug")
# add_missing_domains(co_ug_collection, "co.ug")
# add_missing_domains(or_ug_collection, "or.ug")     
        


    
    