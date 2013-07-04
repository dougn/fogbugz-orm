.. fogbugz-orm documentation master file, created by
   sphinx-quickstart on Sat Jun 29 22:24:43 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================
Welcome to fogbugz-orm's documentation!
========================================


.. include:: ../README.rst


Problems with the FogBugz XML API
========================================

For the most part, the FogBugz XML API is very clean, clean, and easy to use.
However there are some odd corner cases in which the inderlying implementation
is showing through and causing odd inconsistencies which can be problimatic.


#. BeautifulSoup lowercasing all tags and attributes
----------------------------------------------------

Because the FogBugz API Python interface is just a thin wrapper around the
BeautifulSoup HTML/XML parser, the resulting objects returned have all the
elements lower cased. This can be a problem because for bugs and other
objects, these names need to be supplied to the ``cols`` argument with the
mixed case preserved. It also makes it harder to read the resulting python
code, and match it up to the FogBugz XML API documentation.

.. code:: python

    import fogbugz
    
    fb = fogbugz.FogBugz("https://hostname/", secret_token)
    result = fb.search(q="123", cols="sTitle, sPersonAssignedTo, ixArea")
    print result.cases.case.stitle.text
    print result.cases.case.spersonassignedto.text
    ixArea = int(result.cases.case.ixarea.text, 10)
    if ixArea > 10:
        print ixArea

The FogBugzORM preserved the mixed case, and will manage the mixed case and
the cols argument for you, if not supplied.

.. code:: python

    import fborm
    
    fbBugType = dict(
        sTitle = fborm.fbstring,
        sPersonAssignedTo = fborm.fbstring,
        ixArea = fborm.fbint,
    )
    
    fbo = fborm.FogBugzORM("https://hostname/", secret_token)
    result = fbo.search(q='123', casetype=fbBugType)
    print result[0].sTitle
    print result[0].sPersonAssignedTo
    if result[0].ixArea > 10:
        print result[0].ixArea

While more time is required to describe the elements you want returned and
their types. You end up with a more natureal python feel to the interface.
The interface does have a default ``casetype`` argument which is
:py:data:`fborm.objects.fbBug`. Be default it will return and parse all the
elements ddescribed. You can also supply the ``cols`` argument yourself to
return a subset that way.

.. code:: python

    import fborm
    
    fbo = fborm.FogBugzORM("https://hostname/", secret_token)
    result = fbo.search(q='123', cols=cols="sTitle, sPersonAssignedTo, ixArea")
    print result[0].sTitle
    print result[0].sPersonAssignedTo
    if result[0].ixArea > 10:
        print result[0].ixArea



Understanding the Componenets
========================================

XML Element Types
-----------------------------

XML Object Type Mapping
-----------------------------

Parsing XML Data
-----------------------------

FogBugz API Command Wrappers
-----------------------------


FogBugz API Instance Wrapper
-----------------------------


.. _contents:

Core Documentation
========================================

.. toctree::
   :maxdepth: 2
   
   types
   objects
   parse
   commands
   ext
   fborm
   
   util
   version
     
===========   
License
===========

.. include:: ../LICENSE.txt

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

