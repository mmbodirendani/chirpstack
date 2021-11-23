#!/bin/pyhton3

import requests


#print ("we fixed the error request")
from requests.structures import CaseInsensitiveDict
import json
from csv import reader

### Please Change Accordingly
serverAddr = "http://198.199.123.199:8080/"
chirpEmail = "admin"
chirpPassword = "admin"
csvFileName = "C:/Users/omphulusa/Desktop/AIT/Python script/ChirpstackAddBulkDevice/Chripstack Upload.csv"

applicationID = "3"
deviceProfile = "device-profile"
skipFrameCounterCheck = True
deviceActive = True

### Api path
apiJWT = "/api/internal/login"
apiDevice = "/api/devices"

### Get JWT Key
def getJWT(email, password):
    chirpLogin = {"email": email, "password": password}
    keyJWT = requests.post(serverAddr+apiJWT, json=chirpLogin).json()
    return keyJWT['jwt']


### Create Device
def createNewDevice(bearearToken,deviceJSON):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer "+bearearToken
    newDevice = requests.post(serverAddr + apiDevice, data=deviceJSON ,headers=headers).json()


### Prepare Device JSON Data for Appkey
def addNsKey(bearearToken, deviceEUI, appKey, appSkey):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer "+bearearToken

    data = {
        "deviceKeys": {
            "appKey": appSkey,
            "devEUI": deviceEUI,
            "genAppKey": appKey,
            "nwkKey": appSkey
        }
    }
    dataJSON = json.dumps(data)
    urlAppSkey = serverAddr + "/api/devices/" + deviceEUI + "/keys"
    newDevice = requests.post(urlAppSkey, data=dataJSON ,headers=headers).json()

### Prepare Device JSON Data
def deviceJSON(appID, deviceName, deviceDescription, deviceEUI, deviceProfileID ,lotNo, deviceAddress, skipFrameCounterCheck=True, deviceActive=False):
    data = {
        "device": {
            "applicationID": appID,
            "description": deviceDescription,
    	    "devEUI": deviceEUI,
    	    "deviceProfileID": deviceProfileID,
    	    "isDisabled": deviceActive,
    	    "name": deviceName,
    	    "referenceAltitude": 0,
    	    "skipFCntCheck": skipFrameCounterCheck,
    	    "variables": {},
    	    "tags": {
	        "Lot Number": lotNo,
		"Address": deviceAddress
		}
 	 }
    }
    return json.dumps(data)

###Check If Device with same EUI Exist
def ifExist(bearearToken, deviceEUI):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer "+bearearToken
    ifExist = requests.get(serverAddr + apiDevice + "/" + deviceEUI, headers=headers).json()
    try:
        if(ifExist["code"] == 5 or ifExist["code"] == 3):
            return False
    except:
        return True

###Create Devices from CSV file
def chirpAddDevice(csvFile):
    with open(csvFile, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
#            if(ifExist(jwtToken,row[2]) == False):
                addDeviceJSON = deviceJSON(applicationID, row[0], row[1], row[2], deviceProfile, row[3], row[4], skipFrameCounterCheck, deviceActive)
                createNewDevice(jwtToken, addDeviceJSON)
                addNsKey(jwtToken, row[2], row[5], row[6])
#                print("Adding Device:" + row[0] + " , Device EUI: " + row[2])
#            else:
#                print("Device "+ row[0] +" already exsist with EUI:" + row[2])


### Program Start
jwtToken = getJWT(chirpEmail, chirpPassword)
chirpAddDevice(csvFileName)
