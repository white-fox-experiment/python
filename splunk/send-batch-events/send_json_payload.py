import requests
import time
import json

"""
Global Variables
"""
# set splunk variables
url = "https://splunk_url/services/collector/event"
# SECRET Should be encrypted and decrypted
token = '00000000-0000-0000-0000-00000000000'

"""
Functions
"""
def create_payload(records):
    payload = []

    for record in records:
        data = {
                "index" : "test",
                "sourcetype" : 'data_owner:data_grouping:data_type',
                "time" : str(time.time()),
                "event" : record
            }

        payload.append(data)
    
    # Convert list of dicts to string for Splunk
    payload = json.dumps(payload)

    return payload

def submit_splunk_payload(url, token, payload):
  # Set headers
  token = 'Splunk ' + token
  headers = {'Authorization': token}
  
  # Make request to Splunk
  response = requests.post(url, headers=headers, data=payload)
  
  # Error Handling
  if response.status_code != 200 or not requests:
      raise ValueError('Failure: Unable to access Splunk {} {}.'.format(response.status_code, response.reason))
  else:
      print('Success')

"""
Local Testing Variables
"""
records = [{
    "fruit_type": "pineapple",
        "color": "yellow",
        "texture": "rough",
        "properties": ["grows on trees", "has green husk"],
        "sugar_level": "89g"
    },
	{
      "fruit_type": "orange",
      "color": "orange",
      "texture": "smooth",
      "properties": ["grows on bush", "is a type of citrus"],
      "sugar_level": "9g"
    }]
"""
Script starts here
"""
if __name__ == "__main__":
    payload = create_payload(records)
    submit_splunk_payload(url, token, payload)
   
"""
See following file(s) for example(s):
Batch Payload - "sample_event_batch.json"
"""
