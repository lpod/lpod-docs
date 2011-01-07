.. Copyright (c) 2009 Ars Aperta, Itaapy, Pierlis, Talend.

   Authors: Hervé Cauwelier <herve@itaapy.com>
            Jean-Marie Gouarné <jean-marie.gouarne@arsaperta.com>
            Luis Belmar-Letelier <luis@itaapy.com>

   This file is part of Lpod (see: http://lpod-project.org).
   Lpod is free software; you can redistribute it and/or modify it under
   the terms of either:

   a) the GNU General Public License as published by the Free Software
      Foundation, either version 3 of the License, or (at your option)
      any later version.
      Lpod is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
      GNU General Public License for more details.
      You should have received a copy of the GNU General Public License
      along with Lpod.  If not, see <http://www.gnu.org/licenses/>.

   b) the Apache License, Version 2.0 (the "License");
      you may not use this file except in compliance with the License.
      You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0


Documents
==========

.. contents::
   :local:

This manual page describes the ``odf_document``, and the common features of any
``odf_part`` of a ``odf_document``.

Every ``odf_document`` is associated with a ``odf_container`` that encapsulates
all the physical access logic. On the other hand, every ``odf_document`` is
made of several components so-called *parts*. The lpOD API is mainly focused
on parts that describe the global metadata, the text content, the layout and
the structure of the document, and that are physically stored according to an
XML schema. The common lpOD class for these parts is ``odf_xmlpart``.

lpOD provides specialized classes for the conventional ODF XML parts, namely
``odf_meta``, ``odf_content``, ``odf_styles``, ``odf_settings``,
``odf_manifest``.

In order to process particular pieces of content in the most complex parts,
i.e. ``odf_content`` and ``odf_style``, the ``odf_element`` class and its
various specialized derivatives are available. They are described in other
chapters of the lpOD documentation.

Document initialization
------------------------

Any access to a document requires a valid ``odf_document`` instance, that may be
created from an existing document or from scratch, using one of the constructors
introduced below. Once created, this instance gives access to individual parts
through the ``get_part()`` method.

odf_get_document(uri)
~~~~~~~~~~~~~~~~~~~~~~

This function creates a read-write document instance. The returned object is
associated to a physical existing ODF resource, which may be updated. The
required argument is the URI of the resource.

Note: in the present implementation, the URI argument must be either a
file path or a handle corresponding to an open file or socket. The  physical
resource must be a well formed compressed ODF file, such as those natively
produced by OpenOffice.org or compatible office software suites.

Example::

   doc = odf_get_document("C:\MyDocuments\test.odt")

If the ``save()`` method of ``odf_document`` is later used without explicit
target, the document is wrote back to the same resource.

odf_new_document_from_template(uri)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same as ``odf_get_document``, but the ODF resource is used in read only mode,
i.e. it's used as a template in order to generate other ODF physical documents.

Some metadata of the new document are intialized to the following values:

- the creation and modification dates are set to the current date;

- the creator and initial creator are set to the owner of the current process
as reported by the operating system (if this information is available);

- the number of editing cycles is set to 1;

- the idenfication string of the current lpOD distribution is used as the
generator identifier string.

Each piece of metadata may be changed later by the application.

odf_new_document(doc_type)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unlike other constructors, this one generates a ``odf_document`` instance from
scratch. Technically, it's a variant of ``odf_new_document_from_template``, but
the default template (provided with the lpOD library) is used. The required
argument specifies the document type, that must be ``'text'``,
``'spreadsheet'``, ``'presentation'``, or ``'drawing'``. The new document
instance is not persistent; no file is created before an explicit use of the
``save()`` method.

The following example creates a spreadsheet document instance::

   doc = odf_new_document('spreadsheet')

The real content of the instance depends on the default template.

A set of valid template ODF files (created using OpenOffice.org) is
transparently installed with the standard lpOD distribution. Advanced users may
use their own template files. To do so, they have to replace the ODF files
present in the ``templates`` subdirectory of the lpOD installation.

Some metadata are initialized in the same way as with
``odf_new_document_from_template``.

Document MIME type check and control
-------------------------------------

get_mimetype
~~~~~~~~~~~~~

Returns the MIME type of the document (i.e. the full string that identifies
the document type). An example of regular ODF MIME type is::

   application/vnd.oasis.opendocument.text

set_mimetype(new_mimetype)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Allows the user to force a new arbitrary MIME type (not to use in ordinary
lpOD applications !).

Access to individual document parts
------------------------------------

get_part(name)
~~~~~~~~~~~~~~~

Generic C<odf_document> method allowing access to any *part* of a previously
created document intance, including parts that are not handled by lpOD.
The lpOD library provides symbolic constants that represent the ODF usual
XML parts: ``CONTENT``, ``STYLES``, ``META``, ``MANIFEST``, ``SETTINGS`.

This instruction returns the *content* part of a document as a ``odf_content``
object::

   content = document->get_part(CONTENT)

With ``MIMETYPE`` as argument, ``get_part()`` returns the MIME type of the
document as a text string, i.e. the same result as ``get_mimetype()``.

This method may be used in order to get any other document part, such an
image or any other non-XML part. To do so, the real path of the needed part
must be specified instead of one of the XML part symbolic names. As an example,
the instruction below returns the binary content of an image::

   img = document.get_part('Pictures/logo.jpg')

In such a case, the method returns the data as an uninterpreted sequence of
bytes.

(Remember that images files included in an ODF package are stored in a
``Pictures`` folder.)

Returns ``null`` if case of failure.

get_parts
~~~~~~~~~~

Returns the list of the document parts.


Accessing data inside a part
-----------------------------

Everything in the part is stored as a set of ``odf_element`` instances. So, for
complex parts (such as ``CONTENT``) or parts that are not explictly covered in
the present documentation, the applications need to get access to an "entry
point" that is a particular element. The most used entry points are the ``root``
and the ``body``. Every part handler provides the ``get_root()`` and
``get_body()`` methods, each one returning a ``odf_element`` instance, that
provides all the element-based features (including the creation, insertion or
retrieval of other elements that may become in turn working contexts).

For those who know the ODF XML schema, two part-based methods allow the
selection of elements according to *XPath* expressions, namely ``get_element()``
and ``get_element_list()``. The first one requires an XPath expression and a
positional number; it returns the element corresponding to the given position
in the result set of the XPath expression (if any). The second one returns
the full result set (i.e. a list of ``odf_element`` instances). For example,
the instructions below return respectively the first paragraph and all the
paragraphs of a part (assuming ``part`` is a previously selected document
part)::

   paragraph = part.get_element('text:p', 0)
   paragraphs = part.get_element_list('text:p')

Note that the position argument of ``get_element()`` is zero-based, and that it
may be a negative value (if so, it specifies a position counted backward from
the last matching element, -1 being the position of the last one).

So a large part of the lpOD functionality is described with the ``odf_element``
class.

How to persistently update a document
--------------------------------------

Every part may be updated using specific methods that create, change or remove
elements, but this methods don't produce any persistent effect.

The updates done in a given part may be either exported as an XML string, or
returned to the ``odf_document`` instance from which the part depends. With the
first option, the user is responsible of the management of the exported XML
(that can't be used as is through a typical office application), and the
original document is not persistently changed. The second option instructs the
``odf_document`` that the part has been changed and that this change should be
reflected as soon as the physical resource is wrote back. However, a part-based
method can't directly update the resource. The changes may be made persistent
through a ``save()`` method of the ``odf_document`` object.

serialize
~~~~~~~~~~

This part-based method returns a full XML export of the part. The returned XML
string may be stored somewhere and used later in order to create or replace a
part in another document, or to feed another application.

A ``pretty`` named option may be provided. If set to ``TRUE``, this option
specifies that the XML export should be as human-readable as possible.

The example below returns a conveniently indented XML representation of the
content part of a document::

   doc = odf_get_document("C:\MyDocuments\test.odt")
   part = doc.get_part(CONTENT)
   xml = part.serialize(pretty=TRUE)

store
~~~~~~

This part-based method stores the present state (possibly changed) of the part
in a temporary, non-persistent space, waiting for the execution of the next
call of the document-based ``save()`` method.

The following example selects the ``CONTENT`` part of a document, removes the
last paragraph of this content, then sends back the changed content to the
document, that in turn is made persistent::

   content = document.get_part(CONTENT)
   p = content.get_body.get_paragraph(-1)
   p.delete()
   content.store()
   document.save()

Like ``serialize()``, ``store()`` allows the ``pretty`` option.

Note that ``store()`` doesn't write anything on a persistent storage support;
it just instructs the ``odf_document`` that this part needs to be updated.

The explicit use of ``store()`` to commit the changes made in an individual
part is not mandatory. When the whole document is made persistent through the
document-based ``save()`` method, each part is automatically stored by default.
However, this automatic storage may be deactivated using ``needs_update()``.

needs_update(true/false)
~~~~~~~~~~~~~~~~~~~~~~~~

This part-based method allows the user to prevent the automatic storage of
the part when the ``save()`` method of the corresponding ``odf_document`` is
executed.

As soon as a document part is used, either explicitly through the ``get_part()``
document method or indirectly, it may be modified. By default, the document-
based ``save()`` method stores back in the container every part that may have
been used. The user may change this default behaviour using the part-based
``needs_update()`` method, whose argument is ``TRUE`` or ``FALSE``.

In the example below, the application uses the ``CONTENT`` and ``META`` parts,
but the ``META`` part only is really updated, whatever the changes made in
the ``CONTENT``::

   doc = odf_get_document('source.odt')
   content = doc.get_part(CONTENT)
   meta = doc.get_part(META)
   #...
   content.needs_update(FALSE)
   doc.save()

Note that ``needs_update(FALSE)`` deactivates the automatic update only; the
explicit use of the ``store()`` part-based method remains always effective. 

add_file
~~~~~~~~~

This document-based method stores an external file "as is" in the document
container, without interpretation. The mandatory argument is the path of the
source file.

Optional named parameters ``path`` and ``type`` are allowed; ``path`` specifies
the destination path in the ODF package, while ``type`` is the MIME type of the
added resource.

As an example, the instruction below inserts a binary image file available
in the current directory in the "Thumbnails" folder of the document package::

   document.add_file("logo.png", path="Thumbnails/thumbnail.png")

If the ``path`` parameter is omitted, the destination folder in the package is
either ``Pictures`` if the source is identified as an image file (caution: such
a recognition may not work with any image type in any environment) or the root
folder.

The following example creates an entry whose every property is specified::

  document.add_file
    ("portrait.jpg", path="Pictures/portrait.jpg", type="image/jpeg")

The return value is the destination path.

This method may be used in order to import an external XML file as a replacement
of a conventional ODF XML part without interpretation. As an example, the
following instruction replaces the ``STYLES`` part of a document by an arbitrary
file::

   document.add_file("custom_styles.xml", path=STYLES)

Note that the physical effet of ``add_file()`` is not immediate; the file is
really added (and the source is really required) only when the ``save()``
method, introduced below, is called. As a consequence, any update that could be
done in a document part loaded using ``add_file()`` is lost. According to the
same logic, a document part loaded using ``add_file()`` is never available in
the current document instance; it becomes available if the current instance
is made persistent through a ``save()`` call then a new instance is created
using the saved package with ``odf_get_document``.

set_part
~~~~~~~~~

Allows the user to create or replace a document part using data in memory.
The first argument is the target ODF part, while the second one is the source
string.

del_part
~~~~~~~~~

Deletes a part in the document package. The deletion is physically done through
the subsequent call of ``save()``. The argument may be either the symbolic
constant standing for a conventional ODF XML part or the real path of
the part in the package.

The following sequence replaces (without interpretation) the current document
content part by an external content::

   document.del_part(CONTENT)
   document.add_file("/somewhere/stuff.xml", path=CONTENT)

Note that the order of these instructions is not significant; when ``save()``
is called, it executes all the deletions then all the part insertions and/or
updates.

save
~~~~~

This method is provided by the ``odf_document``. If the document instance is
associated with a regular ODF resource available for update (meaning that it
has been created using ``odf_get_container`` and that the user has a write
access to the resource), the resource is wrote back and reflects all the
changes previously committed by one or more document parts using their
respective ``store()`` methods.

As an example, the sequence below updates a ODF file according to changes made
in the ``META`` and ``CONTENT`` parts::

   doc = odf_get_document("/home/users/jmg/report.odt")
   meta = doc.get_part(META)
   content = doc.get_part(CONTENT)
   # meta updates are made here
   meta.store
   # content updates are made here
   content.store
   document.save

However, the explicit call of ``store`` for each individual part is generally
not required knowing that ``store`` is automatically triggered by ``save``
for every used part whose update flag is on.

An optional ``target`` parameter may be provided to ``save()``. If set, this
parameter specifies an alternative destination for the file (it produces the
same effect as the "File/Save As" feature of a typical office software).
The ``target`` option is always allowed, but it's mandatory with
``odf_document`` instances created using a ``odf_new_document_from...``
constructor.


