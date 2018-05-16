""".. _patch:
======================
Monkey Patch
======================

Monkey patch for the fogbugz module to deal with unicode encoding issues
properly in python 2.7 and some python3 versions.

You need to explicitly call monkey_patch() to enable the patch, and do so
before constructing your first FogBugz or FBORM object.

"""
import fogbugz

def __encode_multipart_formdata(self, fields, files):
    """
    fields is a sequence of (key, value) elements for regular form fields.
    files is a sequence of (filename, filehandle) files to be uploaded
    returns (content_type, body)
    """
    BOUNDARY = fogbugz._make_boundary()

    if len(files) > 0:
        fields['nFileCount'] = str(len(files))

    crlf = '\r\n'
    buf = fogbugz.BytesIO()

    for k, v in fields.items():
        vcall = str
        if isinstance(v, unicode):
            vcall = unicode
        if fogbugz.DEBUG:
            print("field: %s: %s"% (repr(k), repr(v)))
        lines = [
            '--' + BOUNDARY,
            'Content-disposition: form-data; name="%s"' % k,
            '',
            vcall(v),
            '',
        ]
        buf.write(crlf.join(lines).encode('utf-8'))

    n = 0
    for f, h in files.items():
        n += 1
        lines = [
            '--' + BOUNDARY,
            'Content-disposition: form-data; name="File%d"; '
                'filename="%s"' % (n, f),
            '',
        ]
        buf.write(crlf.join(lines).encode('utf-8'))
        lines = [
            'Content-type: application/octet-stream',
            '',
            '',
        ]
        buf.write(crlf.join(lines).encode('utf-8'))
        buf.write(h.read())
        buf.write(crlf.encode('utf-8'))

    buf.write(('--' + BOUNDARY + '--' + crlf).encode('utf-8'))
    content_type = "multipart/form-data; boundary=%s" % BOUNDARY
    return content_type, buf.getvalue()

def monkey_patch():
    """Monkey patch (replace/override) the private method
    ``fogbugz.FogBugz._FogBugz__encode_multipart_formdata`` to replace it with
    an alternative version which will properly encode unicode data in fields
    with a sane backoff when mixed unicode pages are encountered.
    """
    fogbugz.FogBugz._FogBugz__encode_multipart_formdata=__encode_multipart_formdata
    
