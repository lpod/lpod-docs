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


Text Fields
===========

.. contents::
   :local:

A `text field` is a special text area, generally short-sized, whose content may
be automatically set, changed or checked by an interactive editor or viewer
according to a calculation formula and/or a content coming from somewhere
in the environment.

A table cell may be regarded as an example of field, according to such a
definition. However, while a table cell is always part of a table row that is in
turn an element in a table, a `text field` may be inserted anywhere in the
content of a text paragraph.

Common field-related features
-----------------------------

Field creation and retrieval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A text field is created "in place" using the ``set_field()`` element-based
method from a text container that may be a paragraph, a heading or a span;
``set_field()`` requires a first argument that specifies the kind of
information to be associated (and possibly displayed) with the field.

Regarding the positioning, this method works in a similar way as
``set_bookmark()`` or ``set_index_mark()`` introduced in the `Text Marks and
Indices` section.

By default, the field is created and inserted  before the first character of
the content in the calling element. As an example, this instruction creates
a ``title`` field (whose role is to display the title of the document) before
the first character of a paragraph::

  paragraph.set_field("title")

A field may be positioned at any place in the text of the host container; to do
so, an optional ``offset`` parameter, whose value is the offset (i.e. character
sequential position) of the target, may be provided. The value of this parameter
is either a positive position, zero-based and counted from the beginning, or a
negative position counted from the end. The following example puts a ``title``
field at the fifth position and a ``subject`` field 5 characters before the
end::

  paragraph.set_field("title", offset=4)
  paragraph.set_field("subject", offset=-5)

The ``set_field()`` method allows field positioning at a position that depends
on the content of the target, instead of a position. Thanks to a ``before`` or
a ``after`` parameter, it's possible to provide a regexp that tells
to insert the new field just before of after the first substring that
matches a given filter. The next example inserts the document subject after a
given string::

  paragraph.set_field("subject", after="this paper is related to ")

More generally, ``set_field()`` allows the same positioning options as
``set_bookmark()`` for simple position bookmarks.

``set_field()`` returns the created ODF element in case of success, or null if
(due to the given parameters and the content of the target container) the field
can't be created.

A text field can't be identified by a unique name or ID attribute and can't be
selected by coordinates in the same way as a cell in a table. However, there is
a context-based ``get_fields()`` method that returns, by default, all the text
field elements in the calling context. This method, when called with a single
argument that specifies the associated content type, returns the fields
that match the given kind of content only, if any. For example, this instruction
returns all the page number fields in the document body::

  document.get_body.get_fields("page number")

Field datatypes
~~~~~~~~~~~~~~~

The value of a field has a data type. The default data type is ``string``, but
it's possible to set any ODF-compliant data type as well, using the optional
parameter ``type``. According to ODF 1.1, §6.7.1, possible types are ``float``,
``percentage``, ``currency``, ``date``, ``time``, ``boolean`` and, of course,
``string``.

If the selected ``type`` is ``currency``, then a ``currency`` additional
parameter is required, in order to provide the conventional currency unit
identifier (ex: EUR, USD). As soon as a ``currency`` parameter is set,
``set_field()`` automatically selects ``currency`` as the field type (so the
``type`` parameter may be omitted).

Note that for some kinds of fields, the data type is implicit and can't be
selected by the applications; in such a situation, the ``type`` parameter, if
provided, is just ignored. For example, a ``title`` or ``subject`` field is
always a string, so its data type is implicit and can't be set.

Common field properties and methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some fields may be created with an optional ``fixed`` boolean parameter, that
is ``false`` by default but, if ``true``, means that the content of the field
should not be automatically updated by the editing applications. For example,
a ``date`` field, that is (by default) automatically set to the current date by
a typical ODF editor each time the document is updated is no longer changed as
long as its ``fixed`` attribute is ``true``. This option is allowed for some
kinds of text fields.

A numeric text field (ex: date, number) may be associated with a display format,
that is identified by a unique name and described elsewhere through a numeric
style; this style is set using the ``style`` parameter with ``set_field()``.

While a field is often inserted in order to allow a viewer or editor to set an
automatically calculated value, it's possible to force an initial content (that
may be persistent if ``fixed`` is true) using the optional ``value`` and/or
``text`` parameters. If the data type is ``string``, the ``value`` is the same
as the ``text``. For a ``date`` or a ``time``, the value is stored in ISO-8601
date format. For other types, the ``value`` is the numeric computable value
of the field. The ``text``, if provided, is a conventional representation of
the value according to a display format.

Text fields use a particular implementation of the generic ``get_text()``
method. When called from a text field element, this method returns the text of
the element (as it could have been set using the ``text`` property), if any.
If the element doesn't contain any text, this method returns the value "as is",
i.e. without formatting.

The generic ``set_text()`` method allows the applications to change the ``text``
content of the element at any time.

Document fields
---------------

According to the ODF vocabulary, document fields are text fields that "can
display information about the current document or about a specific part of the
current document".

This definition could be extended knowing that some so-called document fields
may host contents that are not really informations about the document.

The kind of document field is selected using the mandatory argument of
``set_field()`` or ``get_field()``.

The whole set of allowed document fields is described in the section 6.2 of the
ODF 1.1 specification. Some of them are introduced below with their associated
properties  (the so-called `content key` means the field kind selector that must
be provided when creating a field with ``set_field()``). 

Date fields
~~~~~~~~~~~

Content key: ``date``. Supports ``fixed`` (that should preserve the stored date
from automatic change each time the document is edited).

A date field may contain either the current date or, if "fixed", an arbitrary
other date.

A date field may be adjusted by a certain time period, which is specified using
the ``adjust`` parameter. If the time period is negative, it gets
subtracted from the value of the date field, yielding a date before the current
date. The value of ``adjust`` must be a valid duration.

This example inserts a field that displays the date of the day before
yesterday, due to a ``date adjust`` value that specified a negative value of
48 hours, 0 minutes and 0 seconds::

  paragraph.set_field("date", style="DateStyle", adjust="-PT48H00M00S")

Note that the display format is controlled by the given style (that is, of
course, a date style), and that a date field may be more precise than the date
of the day; whatever the displayed information, a date field is able to store
a full date and time value.

Time fields
~~~~~~~~~~~

Content key: ``time``. Supports ``fixed``.

A time field behaves like a date field, but it stores the current time or an
arbitrary fixed time only. The ``adjust`` parameter, if provided, must be set
with a valid time duration, like with a date field.

Page number fields
~~~~~~~~~~~~~~~~~~

Content key: ``page number``. Supports ``fixed``.

This field displays, by default, the current page number. If ``fixed``, it can
contain an arbitrary other page number. It allows an ``adjust``, telling the
editing applications to display the number of another page, if this page exists.
In addition, it supports a ``select`` argument that may be set to ``current``
(the default), ``previous``, or ``next``, and that specifies if the value is
the number of the current, the previous or the next page.

Page continuation fields
~~~~~~~~~~~~~~~~~~~~~~~~

Content key: ``page continuation``.

This field conditionally displays a continuation string if the current page is
preceded or followed by another page. It requires a ``text`` parameter, that is
the continuation text to display, and a ``select`` parameter, that specifies
what is the page whose existence must be checked.

The example below creates a field that displays "See next page" if and only if
the current page is not the last one::

  paragraph.set_field("page continuation", select="next")

Sender and Author fields
~~~~~~~~~~~~~~~~~~~~~~~~

Content key: various (see below). Supports ``fixed``.

The API allows to set various fields whose purpose is to display in the document
body or in the page headers or footers some informations whose source is not
precisely specified but which regard the so-called "sender" and "author" of the
document. Some of these informations may come from the document metadata.

The general form of the corresponding content keys is ``sender xxx`` or
``author yyy``, where "xxx" may be ``firstname``, ``lastname``, ``initials``,
``title``, ``position``, ``email``, ``phone private``, ``fax``, ``company``,
``phone work``, ``street``, ``city``, ``postal code``, ``country``,
``state or province``, and "yyy" may be ``name`` or ``initials``.

Every sender and author field is created with the appropriate content key and
the optional ``fixed`` flag only.

The following example tells the editing applications to print the initials
of the document sender (if such an information is available) immediately after
a given string::

  paragraph.set_field("sender initials", after="Issued by ")

Of course, every ``sender-`` or ``author-`` field may be ``fixed`` and can
display a given value provided using the ``text`` optional parameter.

Chapter and sheet name fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Content key: ``chapter`` or ``sheet name``.

A chapter field displays the name and/or the number of the current heading in
a document where chapters make sense, while sheet name fields, in spreadsheet
documents, display the name of the current sheet (or table).

For a chapter field, ``set_field()`` allows two parameters, namely ``display``
and ``level``:

- ``display`` specifies the kind of information related to the current chapter
  that the field should display; possible values are ``number``, ``name``,
  ``number-and-name``, ``plain-number``, ``plain-number-and-name`` (see ODF 1.1
  §6.2.7);
- ``level`` is an integer value that specifies the level of the heading that is
  referred to by the field; default is 1.

This examples inserts a field that displays the name of the current level 1
heading::

  paragraph.set_field("chapter", level=1, display="name")

For a sheet name field, no parameter but the ``sheet name`` argument is needed;
the field just displays the name of the current sheet. Note that this field
makes sense for spreadsheet documents only but that the calling element for
``set_field()`` should be a paragraph attached to a cell and not a cell,
knowing that a text fields belongs to a paragraph. Example::

  paragraph.set_field("sheet name")

Declared variable fields
------------------------

A text field may be associated to a so-called "variable", that is, according to
ODF 1.1 (§6.3) a particular user-defined field declared once with an unique name
and used at one or several places in the document. However, the behavior of such
a variable is a bit complex knowing that its content is not set once for all.

A variable may appear with a content at one place, and with a different content
at another place. It should always appear with the same data type. However, the
ODF 1.1 specification is self-contradictory about this question; it tells:

`A simple variable should not contain different value types at different places
in a document. However, an implementation may allow the use of different value
types for different instances of the same variable.`

More precisely, ODF allows several kinds of variables, including so-called
`simple`, `user` and `sequence` variables. The present lpOD level 1 API supports
the two first categories. While a `simple` variable may have different values
(and, practically, different types) according to its display fields, a `user`
variable displays the same content everywhere in the document.

In order to associate a field with an existing variable, ``set_field()`` must be
used with the first argument set to ``variable``, and an additional
``name`` parameter, set to the unique name of the variable, is required. If
the associated variable is a `user` variable, the ``value`` and ``type``
parameters are not allowed. If the variable is `simple`, then it's possible to
set a specific value and/or type, with the effects described hereafter.

The following example sets a field that displays the content of a declared
variable whose name is supposed to be "Amount"::

  paragraph.set_field("variable", name="Amount")

When a field associated to a `simple` variable is inserted using
``set_field()``, its content is set, by default, to the existing content and
type of the variable. If a ``value`` and/or ``text`` parameter is provided, the
field takes this new content, which becomes the default content for subsequent
fields associated to the same variable, but the previous fields keep their
values. The same apply to the field type, if a new ``type`` is provided. Beware,
by `subsequent` and `previous` we mean the fields that precede or follow the
field that is created with a changed content in the order of the document, not
in the order of their creation.

It's possible to insert a variable-based field somewhere without displaying its
value through a text viewer. An optional ``display`` parameter may be set to
``none``, that makes the field invisible, or to ``value`` (the default) to allow
the GUI-based applications to display the value.

On the other hand, all the fields associated to a `user` variable take the same
value. Each time the content of the variable is changed, all the associated
fields change accordingly. The API doesn't allow the application to change this
content through the insertion of an associated field. If needed, the variable
content may be changed explicitly using another method.

If the lpOD-based application needs to install a variable that doesn't exist,
it must use the document-based ``set_variable()`` method, that takes a mandatory
first argument that is its unique name, a ``type`` (whose default is ``string``)
and of course a ``currency`` parameter if ``type`` is ``currency``. Because
``set_variable()`` doesn't set anything visible in the document, it doesn't take
any positioning or formatting parameter. A ``value`` parameter is needed in
order to set the initial content of the variable.

The example below "declares" the variable that is used by a text field in the
previous example::

  document.set_variable("Count", name="Amount", type="float", value=123)

A ``class`` parameter may be provided to select the ``user`` or ``simple`` kind
of variables; the default is ``user``.

A declared variable may be retrieved thanks to its unique name, using the
``get_variable()`` document-based method with the name as argument. The returned
object, if any, supports the generic ``get_properties()`` and
``set_properties()`` method, that allow to get or change its ``value``, ``type``
and ``currency`` parameters. In addition, the variable-specific ``get_value()``
and ``set_value()`` methods are allowed as syntax shortcuts avoiding the use
of ``get_properties()`` and ``set_properties()`` to access the stored values.
