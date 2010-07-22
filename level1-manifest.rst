.. Copyright (c) 2010 Ars Aperta, Itaapy, Pierlis, Talend.

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


Manifest
========

.. contents::
   :local:

The manifest part of a document holds the list of the files included in the
container associated to the ``odf_document``. It's represented by a
``odf_manifest`` object.

Each included file is represented by a ``odf_file_entry`` object, whose
properties are

- ``path``: full path of the file in the container;
- ``type`` : the media type (or MIME type) of the file.

Initialization
--------------

A ``odf_manifest`` instance is created through the ``get_part()`` method of
``odf_document``, with ``MANIFEST`` as part selector::

   manifest = document.get_part(MANIFEST)

Entry access
------------

The full list of manifest entries may be obtained using ``get_entries()``.

It's possible to restrict the list with an optional ``type`` parameter whose
value is a string of a regular expression. If ``type`` is set, then the method
returns the entries whose media type string matches the given expression.

As an example, the first instruction below returns the entries that correspond
to XML parts only, while the next one returns all the XML entries, including
those whose type is not "text/xml" (such as "application/rdf+xml"), and the
last returns all the "image/xxx" entries (whatever the image format)::

   xmlp_entries = manifest.get_entries(type='text/xml')
   xml_entries = manifest.get_entries(type='xml')
   image_entries = manifest.get_entries(type='image')

An individual entry may be selected according to its ``path``, knowing that the
path is the entry identifier. The ``get_entry()`` method, whose mandatory
argument is the ``path``, does the job. The following instruction returns the
entry that stands for a given image resource included in the package (if any)::

   img_entry = manifest.get_entry('Pictures/13BE000002000BDD8EFA.jpg')

Entry creation and removal
--------------------------

Once selected, an entry may be deleted using the generic ``delete`` method.
The ``del_entry()`` method, whose mandatory argument is an entry path, deletes
the corresponding entry, if any. If the given entry doesn't exist, nothing is
done. The return value is the removed entry, or null.

A new entry may be added using the ``set_entry()`` method. This method requires
a unique path as its mandatory argument. A ``type`` optional named parameter
may be provided, but is not required; without ``type`` specification, the media
type remains empty. This method returns the new entry object, or a null value
in case of failure. The example below adds an entry corresponding to an image
file::

   manifest.set_entry('Pictures/xyz.jpg', type = 'image/jpeg')

If ``set_entry()`` is called with the same path as an existing entry, the old
entry is removed and replaced by the new one.

If the entry path is a folder, i.e. if its last character is "/", then the
media type is automatically set to an empty value. However, this rule doesn't
apply to the root folder, i.e. "/", whose type should be the MIME type of the
document.

Beware: adding or removing a manifest entry doesn't automatically add or remove
the corresponding file in the container, and there is no automatic consistency
check between the real content of the part and the manifest.

Entry property handling
-----------------------

An individual manifest entry is a ``odf_file_entry`` object, that is a
particular ``odf_element`` object.

It provides the ``get_path()``, ``set_path()``, ``get_type()``, ``set_type()``
accessors, to get or set the ``path`` and ``type`` properties. There is no check
with ``set_type()``, so the user is responsible for the consistency between the
given type and the real content of the corresponding file. On the other hand,
``set_path()`` fails if the given ``path`` is already used by another entry;
but there is no other check regarding this property, so the user must check the
consistency between the given path and the real path of the corresponding
resource.

If ``set_path()`` puts a path whose last character is "/", the media type of
the entry is automatically set to an empty string. However, for users who know
exactly what they do, ``set_type()`` allows to force a non-empty type *after*
``set_path()``.

