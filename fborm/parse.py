""".. _parsing:

==========================================
FogBugz XML API Data Parsing
==========================================


.. _fborm.parse:

fborm.parse Module Documentation
=================================
"""
import functools
import datetime

def keys2cols(fbtypemap, namemap={}):
    """

    .. code:: python

        res = fb.search(q="1234", cols=keys2cols(fbtypemap, namemap))
        fbobj = extract(res.events.event, fbtypemap, namemap)
        res = fb.edit(**fbargs(fbobj, fbtypemap, namemap))
    """
    return ','.join(namemap.get(getattr(conv, 'colname', name),
                                getattr(conv, 'colname', name))
                    for name, conv in fbtypemap.iteritems()
                    if not name.startswith('_') and
                       not getattr(conv, 'attrib', False))

def fbargs(data, fbtypemap={}, namemap={}):
    """

    .. code:: python

        res = fb.search(q="1234", cols=keys2cols(fbtypemap, namemap))
        fbobj = extract(res.events.event, fbtypemap, namemap)
        res = fb.edit(**fbargs(fbobj, fbtypemap, namemap))
    """
    return dict((str(namemap.get(getattr(fbtypemap.get(name), 'setname', name),
                                 getattr(fbtypemap.get(name), 'setname', name))),
                getattr(fbtypemap.get(name), 'setconvert', fbsetconvert)(value))
                for name, value in data.iteritems()
                if (not name.startswith('_') and
                    getattr(fbtypemap.get(name), 'settable', True)))


def _convert(res, fbdata, name, conv, typemap, namemap):
    mappedname = namemap.get(getattr(conv, 'resname', name),
                             getattr(conv, 'resname', name))

    if getattr(conv, 'ignore', False):
        return
    elif getattr(conv, 'attrib', False):
        res[name] = conv(fbdata, mappedname)
    else:
        inner_data = fbdata.find(mappedname)
        if inner_data is None:
            inner_data = fbdata.find(mappedname.lower())
            if inner_data is None:
                #res[name] = None
                raise RuntimeError('Could not find attribute: ' + repr(mappedname))
        if getattr(conv, 'takes_map', False):
            res[name] = conv(inner_data, namemap)
        elif getattr(conv, 'takes_data', False):
            res[name] = conv(inner_data, res)
        else:
            res[name] = conv(inner_data)
    
def extract(fbdata, fbtypemap, name_map={}):
    """

    .. code:: python

        res = fb.search(q="1234", cols=keys2cols(fbtypemap, namemap))
        fbobj = extract(res.events.event, fbtypemap, namemap)
        res = fb.edit(**fbargs(fbobj, fbtypemap, namemap))
    """
    import jsontree
    res = jsontree.jsontree()
    late_processes = []
    for name, conv in fbtypemap.iteritems():
        if getattr(conv, 'takes_data', False):
            late_processes.append((name, conv))
        else:
            _convert(res, fbdata, name, conv, fbtypemap, name_map)
    for name, conv in late_processes:
        _convert(res, fbdata, name, conv, fbtypemap, name_map)
    return res
    
def extract_all(itemiter, type_map, name_map={}, sort_by=None):
    """
    
    .. code:: python

        res = fb.search(q="1234", cols=keys2cols(fbtypemap, namemap))
        events = extract_all(res.events, fbtypemap, namemap, sort_by='ixBug')
    """
    gen = (extract(item, type_map, name_map) for item in itemiter
           if item != u'\n')
    if not sort_by:
        return list(gen)
    return sorted(gen, key=_sort_by(sort_by))

def _sort_by(names):
    if not isinstance(names, (list, tuple)):
        names = [names]
    def _sort_by_(names, item):
        return [item[name] for name in names]
    return functools.partial(_sort_by_, names)

def _dt2fbdt(dt):
    return dt.isoformat().split('.')[0] + 'Z'
    
def fbsetconvert(value):
    """
    """
    if isinstance(value, datetime.datetime):
        return _dt2fbdt(value)
    if isinstance(value, (tuple, list)):
        return ','.join(fbsetconvert(v) for v in value)
    return unicode(value)
    
    