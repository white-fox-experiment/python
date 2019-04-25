import requests as _requests
import json as _json
import re as _re
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Definitions
def _create_browser():
    """
    This Function Initiates a Browser Instance.
    """
    request = _requests.session()
    #request.proxies['http'] = ''
    request.headers.clear()
    request.headers.update({'Content-Type': 'application/json','Accept': 'application/json'})
    return request

def _get_raw_data(request):
    url = 'http://www.linux-usb.org/usb.ids'
    response = request.get(url, verify=False)

    if not response.ok:
        print("Failed to make the request. {} returned from the server.".format(response.status_code))
        return response
    else:
        rawData = response.text
    return rawData

def _format_raw_data(rawData):
    # Parse each line into a list
    rawData = _re.sub("\\n(?=\\t)", "", rawData)
    rawData = rawData.splitlines()
    lines = [line for line in rawData]

    # Parse lines into a dictionary
    datafeed = []
    for line in lines:
        if len(line) == 0 or line[0] == '#':
            continue
        else:
            vendorJSON = _createVendorJSON(line)
            datafeed.append(vendorJSON)
    return datafeed


def _createVendorJSON(line):
    vendorJSON = {}
    devices = []
    counter = 0
    reformatedData = line.replace("\t", "\n")
    reformatedData = reformatedData.replace("\,", "")
    anyDevices = _re.search("\\n", reformatedData)
    records = reformatedData.splitlines()
    for record in records:
        product = {}
        if counter == 0:
            items = _removeUnwantedChar(record)
            vendorJSON['vendorID'] = items[0]
            vendorJSON['vendorName'] = items[1]
            counter += 1
        else:
            try:
                items = _removeUnwantedChar(record)
                product['productID'] = items[0]
                product['productName'] = items[1]
            except:
                product['productID'] = "N/A"
                product['productName'] = "N/A"
            devices.append(product)
    if anyDevices == None:
        product['productID'] = "N/A"
        product['productName'] = "N/A"
        devices.append(product)
    vendorJSON['devices'] = devices
    return vendorJSON

def _removeUnwantedChar (record):
    item = _re.sub("\s\s", "%$&", record)
    item = _re.sub("\[", "(", item)
    item = _re.sub("\]", ")", item)
    item = _re.sub("\"", " inch", item)
    items = item.split("%$&")     
    return items

def _create_payload(datafeed):
    payload = "{" + f'"vendorProducts" :  ' + _json.dumps(datafeed) + "}"
    return payload
    
def _displayPrettyJSON(payload):
    parsed = _json.loads(payload)
    print(_json.dumps(parsed, indent=2, sort_keys=True))

def usb_json():
  """
  Pull the USB data and return it as JSON
  """
  request = _create_browser()
  rawData = _get_raw_data(request)
  datafeed = _format_raw_data(rawData)
  payload = _create_payload(datafeed)
  _displayPrettyJSON(payload)
  return payload
  
if __name__ == "_main_":
    usb_json()
