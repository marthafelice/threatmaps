import socket
import pymongo


def get_ip_addresses(domain):
    try:
        ips = socket.gethostbyname_ex(domain)
        return ips[2]
    except socket.gaierror:
        return None
   
  

if __name__ == "__main__":    
    myclient = pymongo.MongoClient("mongodb://root:Sf409xqyNL3Eyue@10.10.10.31:27017/?authMechanism=DEFAULT")
    mydb = myclient["ifortify_threat_intelligence"]
    mycol = mydb["subdomains"]
    
    
    for x in mycol.find({}, {"_id": 1, "ip_address":1, "domain":1}):
       
        
        ip_address= get_ip_addresses(x["domain"])
        
        if ip_address != None:    
       
            mycol.update_one({ '_id': x["_id"]},{"$set":{'ip_address' : ip_address}})
            
            
            
          
   