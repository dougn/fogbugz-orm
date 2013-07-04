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

class _obj(object):
    def __init__(self, **args):
        for name, value in args.iteritems():
            setattr(self, name, value)

fbisofmt = "%Y-%m-%dT%H:%M:%SZ"
    
def fbint(data):
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
    strdt = fbstring(data)
    if not strdt:
        return ''
    return datetime.datetime.strptime(strdt, fbisofmt)

def fblistof(conv):
    def _listof(converter, values):
        return [converter(value) for value in values]
    def _extractall(item, data, custom_map):
        return extract_all(data, item, custom_map)
        
    if isinstance(conv, dict):
        call = functools.partial(_extractall, conv)
        call.takes_map = True
    elif callable(conv):
        call = functools.partial(_listof, conv)
    else:
        raise TypeError("Unknown Converter Type")

    call.fbtype = "fborm.types.fblistof"
    return call
    
    
    
def fbcommalistof(fbtype):
    def _fbcommalistof(fbtype, data):
        return [fbtype(_obj(text=value)) for value in
                util.comma_or_space_split(fbstring(data))]
    res = functools.partial(_fbcommalistof, fbtype)
    res.fbtype = "fborm.types.fbcommalistof"
    return res

def fbcol(fbtype, colname=None, resname=None, attrib=False, settable=True,
          setname=None, setter=None):
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
               colname='minievents', resname='minievents', settable=False)
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

    