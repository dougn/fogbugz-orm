""".. _types:

======================
Type Management
======================

Understanding Type Conversion
=============================

Text here listing how it works

.. _fborm.types:

fborm.types Module Documentation
=================================
"""
import re
import functools
import datetime
from . import util
from . import parse

class _obj(object):
    def __init__(self, **args):
        for name, value in args.iteritems():
            setattr(self, name, value)

fbisofmt = "%Y-%m-%dT%H:%M:%SZ"
    
def fbint(data):
    """Type converter for API integer values. 
    
    .. code:: python
    
        fbBug = dict(
            ixBug = fborm.types.fbint,
        )
    
    See `typemapping`_ for more information on the type maps framework.
    
    Some integer fields can be empty, and have special meaning when that
    happens. Here we retun 0 when no data is present as a catchall. In some
    API calls the number 1 is reserverd with special meaning, or can be valid.
    The ixPerson 1 means CLOSED and is not assiciated with a person. While
    on an Area ixPersonPrimaryContact is set to -1 to denote that the
    primary contact should be used. However there is a discrepency between some
    API calls where the list version of a call will return an empty string
    instead of -1. Because this is API call specific, we turn all empty
    strings into 0 for integer fields. Clients need to be aware of these
    discrepencies. This should generalize to ``ixPersonField > 1``
    for evaluating of a field has a valid user id.
    """
    if data.text == '':
        ## some ixPersonFOO items are optional. Default to 0 which means
        ## check elsewhere for the real data. Person 1 also means CLOSED
        ## in some case contexts, so 0 is a special sentinal maning not
        ## supplied.
        return 0
    return int(data.text, 10)

def fbfloat(data):
    return float(data.text)
    
def fbbool(data):
    return data.text == u'true'

def fbstring(data):
    return data.text.encode('utf-8')

def fbdatetime(data):
    """Type converter for API datetime values.
    
    Will return a full python ``datetime.datetime`` object for an API
    datetime value. The ORM will map these values back to strings conforming
    to the FogBugz API. This allows for rich datetime evaluation, comparison
    and modification.
    """
    strdt = fbstring(data)
    if not strdt:
        return ''
    return datetime.datetime.strptime(strdt, fbisofmt)

def fblistof(fbtype):
    """
    """
    def _listof(converter, values):
        if values is None:
            return []
        return [converter(value) for value in values]
    def _extractall(item, data, custom_map):
        return extract_all(data, item, custom_map)
        
    if isinstance(fbtype, dict):
        call = functools.partial(_extractall, fbtype)
        call.takes_map = True
    elif callable(fbtype):
        call = functools.partial(_listof, fbtype)
    else:
        raise TypeError("Unknown Converter Type")

    call.fbtype = "fborm.types.fblistof"
    return call
    
    
    
def fbcommalistof(fbtype):
    """
    """
    def _fbcommalistof(fbtype, data):
        return [fbtype(_obj(text=value)) for value in
                util.comma_or_space_split(fbstring(data))]
    res = functools.partial(_fbcommalistof, fbtype)
    res.fbtype = "fborm.types.fbcommalistof"
    return res


def fbcol(fbtype, colname=None, resname=None, attrib=False,
          gettable=True, settable=True, setname=None, setter=None):
    """
    """
    extractor = functools.partial(fbtype)
    if hasattr(fbtype, 'takes_map'):
        extractor.takes_map = fbtype.takes_map
    if hasattr(fbtype, 'takes_data'):
        extractor.takes_data = fbtype.takes_data
    extractor.attrib=attrib
    if colname:
        extractor.colname=colname
    if resname:
        extractor.resname=resname
    if not settable:
        extractor.settable=False
    if not gettable:
        extractor.ignore=True
    if setname:
        extractor.setname=setname
    if setter:
        extractor.setconvert=setter
    extractor.fbtype = "fborm.types.fbcol"
    return extractor

def fbconditional(converter, **conditions):
    def _conditional(converter, conditions, apidata, objdata):
        if not conditions(objdata):
            return None
        return converter(apidata)
        
    def _conditions(conditions, objdata):
        return all(check(objdata[name])
                   for name, check in conditions.iteritems())
        
    call = functools.partial(
        _conditional, converter, functools.partial(_conditions, conditions))
    call.takes_data = True
    call.fbtype = "fborm.types.fbconditional"
    return call

def fbminievents(eventdict):
    res= fbcol(fblistof(eventdict),
               colname='minievents', resname='events', settable=False)
    res.fbtype = "fborm.types.fbminievents"
    return res

def fbevents(eventdict):
    res = fbcol(fblistof(eventdict),
                colname='events', resname='events', settable=False)
    res.fbtype = "fborm.types.fbevents"
    return res  

def _firstelem(conv):
    def firstelem(conv, data):
        converted = conv(data)
        if isinstance(converted, (list, tuple)):
            if len(converted):
                return converted[0]
            return None
        return converted
    return functools.partial(firstelem, conv)
    
def fblatestevent(eventdict):
    res = fbcol(_firstelem(fblistof(eventdict)),
                colname='latestEvent', resname='events', settable=False)
    res.fbtype = "fborm.types.fblatestevent"
    return res

def fbattr(fbtype):
    def getattr(fbtype, fbdata, name):
        attr = fbdata.get(name)
        if attr is not None:
            return fbtype(_obj(text=attr))
        return attr
    res = fbcol(functools.partial(getattr, fbtype),
                attrib=True, settable=False)
    res.fbtype = "fborm.types.fbattr"
    return res

def _fbselfstr(fbdata, name):
        return fbstring(fbdata)
        
fbself = fbcol(_fbselfstr, attrib=True, settable=False)
""" Special element converter which will convert the parent XML element as
a string. This is needed for when the FogBugz API does not break the data
into sub-taged elements, but instead has only a single piece of string data
in the object, and the remaining data is encoded in attributes on the parent
element. See :py:data:`fborm.objects.fbFilter` for an example of this.
"""
fbself.fbtype = 'fborm.types.fbself'


fbtags = fbcol(fblistof(fbstring),
               colname='tags', resname='tags', setname='sTags',
               setter=parse.fbsetconvert)
"""
:py:data:`fborm.types.fbcol` (:py:data:`fborm.types.fblistof`
(:py:data:`fborm.types.fbstring`),
colname='tags', resname='tags', setname='sTags',
setter= :py:data:`fborm.parse.fbsetconvert`)
               
.. code:: python

    fbtags = fborm.types.fbcol(
        fborm.types.fblistof(fborm.types.fbstring),
        colname='tags',
        resname='tags',
        setname='sTags',
        setter=fborm.parse.fbsetconvert)
"""
fbtags.fbtype = 'fborm.types.fbtags'


fbixBugChildren = fbcol(fbcommalistof(fbint),
                        colname='ixBugChildren',
                        setname='ixBugChildren',
                        setter=lambda x: parse.fbsetconvert(x) if x else ' ')
"""
:py:data:`fborm.types.fbcol` (:py:data:`fborm.types.fbcommalistof`
(:py:data:`fborm.types.fbint`),
colname='ixBugChildren', setname='ixBugChildren',
setter=lambda x: :py:data:`fborm.parse.fbsetconvert` (x) if x else ' ')

.. code:: python

    fbixBugChildren = fborm.types.fbcol(
        fborm.types.fbcommalistof(fborm.types.fbint),
        colname='ixBugChildren',
        setname='ixBugChildren',
        setter=lambda x: fborm.parse.fbsetconvert(x) if x else ' ')

"""
fbixBugChildren.fbtype = 'fborm.types.fbixBugChildren'


def _maybeOpen(filemap):
    result = {}
    for name, fileobj in filemap.iteritems():
        if isinstance(name, unicode):
            name = name.encode('utf-8')
        if isinstance(fileobj, basestring):
            fileobj = open(fileobj, 'rb')
        elif not hasattr(fileobj, 'read'):
            raise TypeError(
                "The 'File' mapping must have values which are "
                "either strings pointing to a file on disk, or "
                "objects with a read() method.")
        result[name] = fileobj
    return result

fbFiles = fbcol(lambda x: None, gettable=False,
                setname='Files',
                setter=_maybeOpen)
"""
:py:data:`fborm.types.fbcol` (lambda x: None,
gettable=False, setname='Files', setter=_maybeOpen)

.. code:: python

    def _maybeOpen(filemap):
        result = dict(filemap)
        for name, fileobj in filemap.iteritmes():
            if isinstance(fileobj, basestring):
                result[name] = open(fileobj, 'rb')
            elif not hasattr(fileobj, 'read'):
                raise TypeError(
                    "The 'File' mapping must have values which are "
                    "either strings pointing to a file on disk, or "
                    "objects with a read() method.")
        return result
    
    fbFiles = types.fbcol(
        lambda x: None,
        gettable=False,
        setname='Files',
        setter=_maybeOpen)

This is used for when you want to upload attachments. The documentation on the
FogBugz API for uploading attachments with FogBugzPy is hidden here:
https://developers.fogbugz.com/default.asp?W208

You need to pass in 'Files' set to a dictionary of file names mapped to
open file handles set for reading in binary mode. To simplify this we treat
this as a dictionary of file names, mapped to file names on disk, and the
:py:data:`fborm.objects.fbFiles` column type converter will convert the on
disk names into open file handles for you.

We are cheating by creating a new dictionary which will go out of scope
and be deleted. This will cause the file handles to be closed implicitly.
Not very clean, but it is safe.

FogBugz has a file size limit which is configurable by administration up to
100Meg. You are responcible for finding out what that limit is set to and
to make sure your files are under that limit.

This should be used as follows:

.. code:: python

    bugType = dict(
        ixBug = fborm.types.fbint,
        Files = fborm.types.fbFiles,
    )

    bug = dict(
        ixBug = 42,
        Files = {
            'somefile.txt': '/place/on/disk/somefile.txt',
            'binary.exe': '/other/place/on/disk/foo.bin',
        }
    )
    
    fbo.edit(bug, bugType)
    
"""
fbFiles.fbtype = 'fborm.types.fbFiles'
