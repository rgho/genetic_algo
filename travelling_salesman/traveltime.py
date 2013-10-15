import urllib2
import json
import string

def travelTimesAndDistance(pFrom,pTo):
	# GET DATA FROM GOOGLE API
	googleApiURL = "http://maps.googleapis.com/maps/api/directions/json?origin=$FROM$&destination=$TO$&sensor=false"
	googleApiURL = string.replace(googleApiURL, "$FROM$", pFrom)
	googleApiURL = string.replace(googleApiURL, "$TO$", pTo)
	apiData = getURL(googleApiURL)
	apiData = json.loads(apiData)

	# GOOD LORD FINDING THE RIGHT KEYS TOOK FOREVER. PULL OUT RELEVANT DATA FROM RETURNED JSON
	status = apiData['status']
	distMeters = apiData['routes'][0]['legs'][0]['distance']['value']
	timeSecs = apiData['routes'][0]['legs'][0]['duration']['value']

	#ERROR HANDLE API CALL STATUS
	if not status=="OK":
		print "API CALL ERROR: " + status

	details = dict()
	details['status'] = status
	details['distance'] = distMeters
	details['time'] = timeSecs

	# DEBUG PRINT
	print status
	print distMeters
	print timeSecs
	
	return details


def statusError(pStatus):
	'''
    OK indicates the response contains a valid result.
    NOT_FOUND indicates at least one of the locations specified in the requests's origin, destination, or waypoints could not be geocoded.
    ZERO_RESULTS indicates no route could be found between the origin and destination.
    MAX_WAYPOINTS_EXCEEDED indicates that too many waypointss were provided in the request The maximum allowed waypoints is 8, plus the origin, and destination. ( Google Maps API for Business customers may contain requests with up to 23 waypoints.)
    INVALID_REQUEST indicates that the provided request was invalid. Common causes of this status include an invalid parameter or parameter value.
    OVER_QUERY_LIMIT indicates the service has received too many requests from your application within the allowed time period.
    REQUEST_DENIED indicates that the service denied use of the directions service by your application.
    UNKNOWN_ERROR indicates a directions request could not be processed due to a server error. The request may succeed if you try again.
	'''
	
	if status == "OK":
		return False
	elif status == "NOT_FOUND":
		return True
	elif status == "ZERO_RESULTS":
		return True
	elif status == "MAX_WAYPOINTS_EXCEEDED":
		return True
	elif status == "INVALID_REQUEST":
		return True
	elif status == "OVER_QUERY_LIMIT":
		return True
	elif status == "REQUEST_DENIED":
		return True

def getURL(url):
	try:
		result = urllib2.urlopen(url)
		return result.read()
	except urllib2.URLError, e:
		return "ERROR WITH URL: " + str(e) 


#travelTimesAndDistance("Toronto", "Montreal")




