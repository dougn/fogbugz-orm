"""
==========================================
Utility Functions (fborm.util)
==========================================

"""
import re
import os

_re_coma_or_space_sep = re.compile('(?:\s*,\s*)+|\s+')

def comma_or_space_split(sdata):
    """smart comma splitting that can deal with empty sets.

    >>> comma_or_space_split(' asdf, ,, a   df , ,,   sad f,')
    ['asdf', 'a', 'df', 'sad', 'f']
    >>> comma_or_space_split(',asdf,')
    ['asdf']
    >>> comma_or_space_split(' asdf ')
    ['asdf']
    """
    return [x for x in _re_coma_or_space_sep.split(sdata) if x]

_shared_connection = None
def _connection():
    global _shared_connection
    if _shared_connection is None:
        import httplib2
        _shared_connection = httplib2.Http()
    return  _shared_connection

def download(url):
    response, content = _connection().request(url)
    if response.status != 200:
        raise RuntimeError("URL (%s) returned status code %d: %s" %
                           (url, response.status, response.reason))
    return content

def download_to_file(url, filename):
    try:
        data = download(url)
        fn = open(filename, 'wb')
        fn.write(data)
        fn.close()
    except Exception, e:
        if os.path.exists(filename) and os.path.isfile(filename):
            try:
                os.unlink(filename)
            except:
                pass
        raise e
    