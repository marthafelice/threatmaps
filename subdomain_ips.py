import socket
import pymongo


def get_ip_addresses(subdomain):
    try:
        ips = socket.gethostbyname_ex(subdomain)
        return ips[2]
    except socket.gaierror:
        return None
   
  

if __name__ == "__main__":    
    myclient = pymongo.MongoClient("mongodb://root:Sf409xqyNL3Eyue@10.10.10.31:27017/?authMechanism=DEFAULT")
    mydb = myclient["ifortify_threat_intelligence"]
    mycol = mydb["subdomains"]
    
 
    
    for x in mycol.find({}, {"_id": 1, "ip_address":1, "subdomains":1}):
 
        # ip_address= get_ip_addresses(x["subdomain"])
        # print(x["subdomains"])
        counter = 0
        for y in x["subdomains"]:
            ip_address= get_ip_addresses(y["value"])
            print(y["value"])
            print(ip_address)
        
            if ip_address != None:    
        
                mycol.update_one({ '_id': x["_id"]},{"$set":{'subdomains.'+str(counter)+'.ip_address' : ip_address}})
            
            counter = counter + 1
            
            
            
          
   