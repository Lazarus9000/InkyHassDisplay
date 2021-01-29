import requests
import json

#Read token
f = open("token.txt", "r")
token = f.read()
print(token)

#Get state
API_ENDPOINT = "http://192.168.1.208/api/states/sensor.restaffald_tid"
  
# data to be sent to api 
data = {'Authorization':"Bearer " + token, 
        'Content-Type':'application/json'} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
print(r.text)

#Deserialize JSON
object = json.loads(r.text);
print(object)

print(object.state)

#Draw value on display

#Success!
