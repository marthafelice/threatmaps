
import pymongo
import whois

    
def get_whois_data(domain):
    try:
        return whois.whois(domain)
    except whois.parser.PywhoisError:
        return None 

if __name__ == "__main__":    
    myclient = pymongo.MongoClient("mongodb://root:Sf409xqyNL3Eyue@10.10.10.31:27017/?authMechanism=DEFAULT")
    mydb = myclient["the_eagle"]
    mycol = mydb["Domains"]
    
    
    for document in mycol.find({}, {"_id": 1, "Domain": 1}):
        domain = document["Domain"]
    
        whois_data = get_whois_data(domain)
        try:
            whois_data['org']
        except KeyError:
            print("Organisation key not defined")
        else:
            if whois_data['org'] == None or whois_data['org'] == 'UNKNOWN':
                whois_data = []
                
            mycol.update_one({ '_id': document["_id"]},{"$set":{'who_is_data' : whois_data}})



   

   