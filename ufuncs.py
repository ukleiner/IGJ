def empty(string):
    return string is None or len(string.strip()) == 0

def find_file(self, url):
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
        req = requests.head(url)
        if req.status_code == 200:
            return url

    return None
