import requests

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
Script starts here
"""
if __name__ == "__main__":
    submit_splunk_payload(url, token, payload)
