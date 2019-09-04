import json
import csv
import time
import datetime
import urllib.request
"""This package contains all the functions necessary for the TCAT Skill to work.
Author: Jonathan Duque
Date: 4/6/19
"""
    
"""Utilizes Google Maps API to retrieve all possible bus routes from the origin point to the destination point.
Returns the data generated in json format.
Precondition: org must be a string, dest must be a string
"""
def generateJson(org, dest):
    assert type(org) == str
    assert type(dest) == str
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyBvN8Tv8Exp0XVvt0evPXxef0qusCkov2U'
    mode = 'transit'
    transit_mode = 'bus'
    origin = org.replace(' ','+')
    destination = dest.replace(' ','+')
    nav_request = 'origin={}&destination={}&mode={}&transit_mode={}&key={}'.format(origin,destination,mode,transit_mode,api_key)
    request = endpoint + nav_request
    response = urllib.request.urlopen(request).read()
    directions = json.loads(response)
    return directions


"""Generates a Json File given a dictionary.
Precondition: jsonDump must be a dictionary
"""
def generateJsonFile(jsonDump):
    with open('data2.txt', 'w') as f:
        json.dump(jsonDump, f, sort_keys = True, indent = 4, ensure_ascii=False)

"""Reads a Json file and stores the information as a valid dictionary.
Returns the dictionary."""
def readJsonFile():
    with open('data.txt') as json_file:
        data = json.load(json_file)
    return data

"""This function is used for debugging purposes only. It reads a Json file in
and parses the relevant information from it."""
def debugParseJson():
    data= readJsonFile()
    feeder = parseJson(data)
    return feeder

"""This function returns an appropriate message depending upon the status of the
json returned
Precondition: json must be a valid json dictionary""" 
def checkErrors(json):
    if json['status'] == 'OK':
        return 'OK'
    if json['status'] == 'OVER_DAILY_LIMIT':
        return 'Server error, please try again later.'
    if json['status'] == 'OVER_QUERY_LIMIT':
        return 'Server is currently down'
        
    return 'There was a problem with one of the parameters you mentioned. Please try again.'
    
"""Parses the json for important bus route information.
Precondition: directions must be a valid dictionary"""
def parseJson(directions):
    legs = directions['routes'][0]['legs']
    busObject = legs[0]['steps']

    track = False
    for val in range(0,len(busObject)):
        if 'transit_details' in busObject[val].keys():
            busObject = busObject[val]['transit_details']
            track = True
            break

    if track == False:
        return ['Failure']
    
    deptStop = busObject['departure_stop']['name']
    deptTime = busObject['departure_time']['text']
    busNum = busObject['line']['short_name']
    busFeeder = [busNum, deptStop, deptTime]
    return busFeeder

#figures out how many minutes remaining till bus departure
def calculateTime(futureTime):
    currentTime = datetime.datetime.now().time()
    

    return

#creates sentence for alexa to utter
def createInformation(feeder):
    liner = "Next " + feeder[0] + " bus departs at " +feeder[1] + " at "+feeder[2]
    return liner


    
    
    
