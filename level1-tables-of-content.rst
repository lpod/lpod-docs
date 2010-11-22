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


Tables of contents
==================

.. contents::
   :local:

A table of contents (TOC) is represented by an ``odf_toc`` object, which is
created using the ``odf_create_toc()`` constructor.

TOC creation
------------

A table of contents is created as a free element using the ``odf_create_toc()``
constructor, with a mandatory unique name as its first argument, and the
following parameters:

- ``title``: an optional title (to be displayed at the TOC head), whose
  default value is the given name;
- ``style``: the name of a section style applying to the TOC;
- ``protected``: a boolean flag that tells the editing applications if the
  section is write-protected (default=``true``);
- ``outline level``: specifies the last outline level to be used used when
  generating the TOC from headings; if this parameter is omitted, all the
  outline levels are used by default;
- ``use outline``: a boolean flag that specifies if the TOC must be generated
  from headings (default=``true``);
- ``use index marks``: a boolean flag that specifies if the TOC must be
  generated from index marks (default=``false``).

A table of contents object, after creation, may be put somewhere in a
document using a generic method such as ``insert_element()``.


TOC retrieval
-------------

An existing table of contents may be retrieved by name using the context
method ``get_toc()``.

It's possible to retrieve the full list of the TOCs in a context through
``get_tocs()``, without argument.


TOC methods
-----------

The ``odf_toc`` elements provide the following methods:

- ``get_name()`` and ``set_name()`` to get or set the internal unique name;
- ``get_title()`` and ``set_title()`` to get or change the display TOC title;
with ``set_title()``, the first argumentis the text of the title, and a
``style`` named parameter is allowed to specify a paragraph style for the title;
- ``get_outline_level()`` and ``set_outline_level()`` to get or change the
  current outline level property;
- ``get_use_outline()`` and ``set_use_outline()`` to get or set the use outline
  flag;
- ``get_use_index_marks()`` and ``set_use_index_marks()`` to get or set the use
  index marks flag;
- ``get_formatted_text()``: returns the plain text content of the TOC, with some
  formatting features;
- ``fill``: builds the body of the TOC according to the content of a given
  document and the TOC parameters.

The ``fill`` method does an effective generation of the TOC content according to
the current content of a document. Beware, this method is far less rich than the
TOC generation feature of a typical interactive text processor, so it should be
use if an automatic TOC generation is required only.

As long as the ``odf_toc`` object is not attached to a ``odf_document``,
the ``fill`` method requires an ODF document as argument. If the object belongs
to a document and if the argument is omitted, the content of the TOC is
generated from the content of the host document. However, it's possible to
insert a TOC in a document then ``fill`` it using the content of another
document: the ``fill`` method generates a content according to the document
provided as argument, if any.

The TOC is populated by ``fill`` using the outline (i.e. the hierarchical
headings of the document), the TOC index marks, or both, according to the
corresponding flags. Note that ``fill`` can't generate any content if both
``use outline`` and ``use index marks`` are ``false``.

