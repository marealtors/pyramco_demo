# pyramco
# version 0.9.1

# a complete wrapper class for RAMCO API calls
# requires Python 3.6+ and the 'requests' module
# set your RAMCO api key in a separate file 'config.py' as 'ramco_api_key'
# documentation on the RAMCO API at: https://api.ramcoams.com/api/v2/ramco_api_v2_doc.pdf

# imports
import json
import requests
import config

# the base RAMCO API url is always the same
ramco_api_url = 'https://api.ramcoams.com/api/v2/'


# pyramco wrapper operations

## metadata operations

### get_entity_types
# no arguments are accepted. fetches all entities in the system.

def get_entity_types():
	payload = {
		'key': config.ramco_api_key,
		'Operation':'GetEntityTypes'
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)

### get_entity_metadata
# accepts a valid entity name enclosed in apostrophes, like: 'Contact' returns all metadata on that entity.

def get_entity_metadata(entity):
	payload = {
		'key': config.ramco_api_key,
		'Operation':'GetEntityMetadata',
		'Entity': entity
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)

### get_option_set
#accepts a valid entity name and a single attribute. returns value/label pairs for the specified OptionSet.
def get_option_set(entity, attribute):
	payload = {
		'key': config.ramco_api_key,
		'Operation':'GetOptionSet',
		'Entity': entity,
		'Attribute': attribute
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)

### clear_cache
# no arguments are accepted. clears the server-side metadata cache

def clear_cache():
	payload = {
		'key': config.ramco_api_key,
		'Operation':'ClearCache'
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)


## data querying operations

### get_entity
# accepts a valid entity name, GUID, and a tuple of comma-separated attribute names, returns attribute values for the specified contact matching the GUID
def get_entity(entity, guid, *attributes):
	payload = {
		'key': config.ramco_api_key,
		'Operation':'GetEntity',
		'Entity': entity,
		'GUID': guid,
		'Attributes': attributes
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)

### get_entities
# accepts a valid entity name, a tuple of comma-separated attribute names, and (optionally) a valid filters string, a string delimiter character, and an integer value for the max results.
def get_entities(entity, *attributes, filters='', string_delimiter='', max_results=''):
	payload = {
		'key': config.ramco_api_key,
		'Operation':'GetEntities',
		'Entity': entity,
		'Filter': filters,
		'Attributes': attributes,
		'StringDelimiter': string_delimiter,
		'MaxResults': max_results
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)

### resume_streamtoken
# accepts a valid streamtoken string and resumes the get_entities request that generated it.
def resume_streamtoken(streamtoken):
	payload = {
		'key': config.ramco_api_key,
		'Operation':'GetEntities',
		'StreamToken': streamtoken
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)

### validate_user
# accepts a username and password. for valid combinations, returns that Contact's guid. for invalid combinations, returns 422 error.
def validate_user(username, password):
	payload = {
		'key': config.ramco_api_key,
		'Operation':'ValidateUser',
		'cobalt_username ': username,
		'cobalt_password': password
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)


## data transformation operations

### update_entity
# accepts a valid entity name + guid, a tuple of comma separated attribute=value pairs, and optionally a string delimiter character

def update_entity(entity, guid, *attributes, string_delimiter=''):
	payload = {
		'key': config.ramco_api_key,
		'Operation':'UpdateEntity',
		'Entity': entity,
		'Guid': guid,
		'AttributeValues': attributes,
		'StringDelimiter': string_delimiter
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)

### create_entity
# accepts a valid entity name, a tuple of comma separated attribute=value pairs, and optionally a string delimiter character
def create_entity(entity, *attributes, string_delimiter=''):
	payload = {
		'key': config.ramco_api_key,
		'Operation':'CreateEntity',
		'Entity': entity,
		'AttributeValues': attributes,
		'StringDelimiter': string_delimiter
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)

### delete_entity
# accepts a guid and deletes the corresponding record
def delete_entity(entity, guid):
	payload = {
		'key': config.ramco_api_key,
		'Operation':'DeleteEntity',
		'Entity': entity,
		'GUID': guid
		}
	reply = requests.post(ramco_api_url,payload).json()
	return(reply)

# end pyramco wrapper operations


## code/error handling section (DRAFT)

# definitions

code_200 = {'description_short':'OK', 'description_verbose':'The request was successfully processed and data is included in the response'}
code_204 = {'description_short':'OK: No Data','description_verbose':'The request was successfully processed but no data is included in the response. This is typical of UpdateEntity requests.'}
code_206 = {'description_short':'OK: Partial Data','description_verbose':'The request was successfully processed and partial data is included in the response. This is the expected response when the dataset that Ramco needs to return to the user is too large. A StreamToken will be returned to allow the user to fetch the remaining data.'}
code_400 = {'description_short':'Bad Request','description_verbose':'The request was not understood. See the response text for more information.'}
code_401 = {'description_short':'Unauthorized','description_verbose':'The request was understood but it will not be fulfilled due to a lack of user permissions. See the response text for more information.'}
code_404 = {'description_short':'Not Found','description_verbose':'The request is understood but no matching data is found to return.'}
code_422 = {'description_short':'Invalid User','description_verbose':'No user with provided username/password combination. This error is specific to the AuthenticateUser request.'}
code_500 = {'description_short':'Server Error','description_verbose':'Something is not working correctly server-side. This is not an issue that can be resolved by modifying query syntax.'}
code_unknown = {'ResponseCode':999,'description_short':'Unknown Internal/pyramco Error','description_verbose':'No code or response returned from RAMCO. Verify you are on Python version 3.6+. Check your connections and settings. This error originates in your code or pyramco itself.'}

# function

def handler(reply):
	if reply['ResponseCode'] == 200: # returns unmodified results
		return(reply)

	elif reply['ResponseCode'] == 204: # returns unmodified results
		return(reply)

	#elif reply['ResponseCode'] == 206: # iterates through all paged results via streamtoken and returns them combined
		#return(reply)

	elif reply['ResponseCode'] == 400: # returns results plus additional error text from documentation
		return(reply)

	elif reply['ResponseCode'] == 404: # returns results plus additional error text from documentation
		return(reply)

	elif reply['ResponseCode'] == 422: # returns results plus additional error text from documentation
		return(reply)

	elif reply['ResponseCode'] == 500: # returns results plus additional error text from documentation
		return(reply)

	else: # returns the text for other/unknown errors
		return(code_unknown)