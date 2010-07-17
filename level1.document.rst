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
``odf_manifest``; some of them provide methods dedicated to get or set the
document metadata.

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

odf_new_document_from_type(doc_type)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unlike other constructors, this one generates a ``odf_document`` instance from
scratch. Technically, it's a variant of ``odf_new_document_from_template``, but
the default template (provided with the lpOD library) is used. The required
argument specifies the document type, that must be ``'text'``,
``'spreadsheet'``, ``'presentation'``, or ``'drawing'``. The new document
instance is not persistent; no file is created before an explicit use of the
``save()`` method.

The following example creates a spreadsheet document instance::

   doc = odf_new_document_from_type('spreadsheet')

The real content of the instance depends on the default template.

A set of valid template ODF files (created using OpenOffice.org) is
transparently installed with the standard lpOD distribution. Advanced users may
use their own template files. To do so, they have to replace the ODF files
present in the ``templates`` subdirectory of the lpOD installation.

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

