'''Basic Modules'''
import requests
import json
from base64 import b64encode, b64decode
import math

'''Format Text Modules'''
from bs4 import BeautifulSoup
import html2text
from html2json import collect
from urllib.parse import urlencode

'''Importatnt Toubleshooting Modules'''
from retry import retry

'''Basic CORE Functions'''
def initalize_request_session():
    '''
    Function creates a request session
    '''
    session = requests.session()

    return session

def update_request_session(session, **kwargs):
    # Function takes session and any arguments and updates/sets session attributes 
    for key, value in kwargs.items():
        for attr in session.__attrs__:
            if attr == key:
                setattr(session, attr, value)
    return session

@retry(tries = 3)
def handle_request_response(response):
    if response.status_code != 200:
        # Take response html and format
        response_html = convert_html_to_text(beautify_html(response.text))
        message = 'Additional Details: {}'.format(response_html)
        raise Exception('FAILED: Unable to complete requests recieved {}:{}\n\n{}'.format(response.status_code, response.reason, message))
    else:
        parsed = extract_and_parse_data(response)
        return parsed

def base64_encode(username, password):
    # Put into base64(username:password)
    string = '{}:{}'.format(username, password)
    string_to_byte = string.encode()
    token = b64encode(string_to_byte)

    # Convert from byte to string
    token = token.decode()

    return token

def base64_decode(token):
    # Determine if String or Byte
    if type(token) == bytes:
        byte = b64decode(token)
        byte_to_string = byte.decode()
        auth = byte_to_string
    elif type(token) == str:
        string_to_byte = token.encode()
        byte = b64decode(string_to_byte)
        auth = byte.decode()
    else:
        auth = None

    return auth

'''End Of Basic CORE Functions'''

def determine_total_pages(total, limit):
    total_pages = math.ceil(total/limit)
    total_pages = range(total_pages + 1)

    return total_pages

'''Functions for Formating Data'''
def convert_html_to_text(value):
    h = html2text.HTML2Text()
    h.ignore_links = True
    value = h.handle(value)

    return value

def beautify_html(value):
    soup = BeautifulSoup(value).h1
    if soup != None:
        prettyHTML = soup.prettify()
        return prettyHTML
    else:
        return value

def convert_table_to_json(parsed):
    table_data = [[cell.text for cell in row("td")] for row in BeautifulSoup(parsed)("tr")]
    table_data = json.dumps(dict(table_data))
    return table_data

def convert_dict_to_urlencoded(value):
    value = '?' + urlencode(value)
    return value

def extract_and_parse_data(response):
    response_content_type = (json.loads(json.dumps(response.headers._store)))['content-type'][1]
    extracted_raw_data = response.text
    if "text/html" in response_content_type:
        parsed = BeautifulSoup(extracted_raw_data)
    elif "application/json" in response_content_type:
        parsed = json.loads(extracted_raw_data)
    else:
        parsed = extracted_raw_data

    return parsed

'''End of Functions for Formating Data'''
