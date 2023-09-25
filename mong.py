import socket
import pymongo
import whois
def resolve_ip_to_domain(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return None
    
def get_whois_data(domain):
    return whois.whois(domain)   

if __name__ == "__main__":    
    myclient = pymongo.MongoClient("mongodb://root:Sf409xqyNL3Eyue@10.10.10.31:27017/?authMechanism=DEFAULT")
    mydb = myclient["ifortify_threat_intelligence"]
    mycol = mydb["uganda_ip_addresses"]
 
    ip_address =  mycol.find({'domains':{'$ne':[]}},{ "_id": 0, "ip_str": 1 })

    for x in ip_address:
        
        # domain=resolve_ip_to_domain(x["ip_str"])
        domain=x["ip_str"]
        whois_data = get_whois_data(domain)
        if whois_data:
            whois_data['creation_date'] =str(whois_data['creation_date'])
            whois_data['expiration_date'] =str(whois_data['expiration_date'])
            whois_data['updated_date'] =str(whois_data['updated_date'])
            print(whois_data)
        else:
            print("Failed to retrieve WHOIS data.")        
        if domain != None:    
            data_to_insert={'ip_address':x["ip_str"],'domain':domain, 'who-is-data':whois_data}
            newcol = mydb["uganda_ips_and_domains"]
            rec_id1 = newcol.insert_one(data_to_insert)
            
   