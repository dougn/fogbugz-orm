
import fborm.objects
import sphinx.domains.python
from sphinx.locale import l_, _

kvp_names = ('keyvaluepair', 'kvp', 'item', 'key', 'keyval')

## Yes, I am EVIL!!!
sphinx.domains.python.PyObject.doc_field_types.append(
    sphinx.domains.python.TypedField('keyval', label=l_('Key (Value)'),
           names=kvp_names,
           typerolename='obj', typenames=('value', 'val'),
           can_collapse=True),
)

registry = {}

def get_overrides(lines):
    res = {}
    outlines = []
    for line in lines:
        if any(line.strip().startswith(':'+n) for n in kvp_names):
            pre, param, doc = line.split(':', 2)
            paramdata = param.strip().split()
            keyname = paramdata[-1]
            typeover = ''
            if len(paramdata) == 3:
                typeover = paramdata[1]
            res[keyname] = dict(type=typeover, doc=doc)
        else:
            outlines.append(line)
    return res, outlines

def object_dicts_docstring(app, what, name, obj, options, lines):
    if (what is not 'data' or
        not name.startswith('fborm.objects.') or
        name not in registry):
        return
    overrides, outlines = get_overrides(lines)
    obj = registry[name]
    lines[:] = []
    for key, value in sorted(obj.iteritems()):
        vtype = ''
        vdoc = ''
        
        if key in overrides:
            vtype = overrides[key]['type']
            vdoc = ' ' + overrides[key]['doc']

        if not vtype:
            if hasattr(value, 'fbtype'):
                vtype = value.fbtype
            elif hasattr(value, '__module__'):
                vtype = value.__module__ + '.' + value.__name__
            elif hasattr(value, '__class__'):
                vtype = value.__class__.__module__+'.'+value.__class__.__name__
            else:
                vtype = ''
        
        lines.append(':kvp ' + vtype + ' ' + key + ':' + vdoc)
    lines.append('')
    lines.extend(outlines)
    #print name, lines

class FakeTypeElem(object):
    def __repr__(self):
        return 'fborm.types.<fbcastfunc>'

class DotDotDot(object):
    def __init__(self, quoted):
        self.quoted = quoted
    def __repr__(self):
        if self.quoted:
            return repr('...')
        return '...'

faketypeelem = FakeTypeElem()
dotdotdot = DotDotDot(False)
kddd = DotDotDot(True)
object_dict = {
    'apiKey': faketypeelem,
    kddd: dotdotdot
}


def command_function_signture(
    app, what, name, obj, options, signature, return_annotation):
    if (what is not 'data' or
        not name.startswith('fborm.objects.') or
        not isinstance(obj, dict)):
        return signature, return_annotation
    if not all(callable(v) for v in obj.itervalues()):
        return signature, return_annotation
    registry[name] = dict(obj)
    for name in obj.keys():
        del obj[name]
    obj.update(object_dict)
    return None, None

def setup(app):
    app.connect('autodoc-process-docstring', object_dicts_docstring)
    app.connect('autodoc-process-signature', command_function_signture)
    
