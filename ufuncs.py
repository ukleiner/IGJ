import warnings
from os import path
from urllib.parse import urlparse

import requests
from requests.exceptions import ConnectionError

def empty(string):
    return string is None or len(string.strip()) == 0

def find_file(url):
    '''
    Checks if the file can be found

    Parameters
    ---------
    url - URL to the file

    Returns
    ------
    str
    The file if can be found, None otherwise
    '''
    if empty(url):
        return None

    parsed = urlparse(url)
    scheme = parsed.scheme
    if scheme == '':
        if path.isfile(url):
            return url
    elif scheme in ['https', 'http']:
        # Only headers
        # allow_redirects = False by default
        try:
            req = requests.head(url)
            if req.status_code == 200:
                return url
            else:
                warnings.warn(f"File not found, status code {req.status_code}")
        except ConnectionError as e:
            warnings.warn(f"Couldn't connect to  {url}")
            return None

    return None
