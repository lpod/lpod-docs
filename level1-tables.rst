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

Tables
=======

.. contents::
   :local:


An ``odf_table`` object is a structured container that holds two sets
of objects, a set of *rows* and a set of *columns*, and that is
optionally associated with a table style.

The basic information unit in a table is the *cell*. Every cell is
contained in a row. Table columns don't contain cells; an ODF column
holds information related to the layout of a particular column at the
display time, not content data.

A cell can directly contain one or more paragraphs. However, a cell
may be used as a container for high level containers, including lists,
tables, sections and frames.

Every table is identified by a name (which must be unique for the
document) and may own some optional properties.

Table creation and retrieval
----------------------------
A table is created using ``odf_create_table()`` with a mandatory name
as its first argument and the following optional parameters:

- ``width``, ``length``: the initial size of the new table
  (rows then columns), knowing that it's zero-sized by default
  (beware: because cells are contained in rows, no cell in created if
  as long as ``width`` is less than 1);
- ``size``: specifies a length and a width (in this order) as a single string
  (the two values are comma-separated); may replace ``length`` and ``width``;
- ``style``: the name of a table style, already existing or to be
  defined;
- ``cell style``: the style to use by default for every cell in the table;
- ``protected``: a boolean that, if true, means that the table should
  be write-protected when the document is edited through a user-oriented,
  interactive application (of course, such a protection doesn't prevent
  an lpOD-based tool from modifying the table)(default is false);
- ``protection key``: a (supposedly encrypted) string that represents
  a password; if this parameter is set and if ``protected`` is true,
  a end-user interactive application should ask for a password that matches
  this string before removing the write-protection (beware, such a protection
  is *not* a security feature);
- ``print``: boolean, tells that the table should be printable; default is true;
- ``print ranges``: the cell ranges to be printed, if some areas are not to
  be printed; the value of this parameter is a space-separated list of cell
  ranges expressed in spreadsheet-style format (ex: "E6:K12").

Once created, a table may be incorporated somewhere using ``insert_element()``.

The style of a table may be retrieved or changed at any time using the generic
``get_style()`` and ``set_style()`` accessors.

A table may be retrieved in a document according to its unique name using
the context-based ``get_table_by_name()`` method with the name as argument.
It may be selected by its sequential position in the list of the table
belonging to the context, using ``get_table_by_position()``, with a zero-based
numeric argument (possibly counted back from the end if the argument is
negative). A ``get_table()`` method is provided, that works like
``get_table_by_position()`` if the argument is numeric or like
``get_table_by_name()`` otherwise (of course, if the name of the desired table
looks like a number, there is no choice but ``get_table_by_name()`` to retrieve
it by name). Without argument, ``get_table()`` returns the first table in the
context (if any). In addition, it's possible to retrieve a table according to
its content, through ``get_table_by_content()``; this method returns the first
table (in the order of the document) whose text content matches the given
argument, which is regarded as a regular expression.

Table content retrieval
-----------------------

A table object provides methods that allow to retrieve any column, row or cell
using its logical position. A position may be expressed using either zero-based
numeric coordinates, or alphanumeric, spreadsheet-like coordinates. For example
the top left cell should be addressed either by [0,0] or by "A1". On the other
hand, numeric coordinates only allow the user to address an object relatively to
the end of the table; for example, [-1,-1] designates the last cell of the last
row whatever the table size.

Table object selection methods return a null value, without error, when the
given address is out of range.

The number of rows and columns may be got using ``get_size()``.

An individual cell is selected using ``get_cell()`` with either a pair of
numeric arguments corresponding to the row then the columns, or an alphanumeric
argument whose first character is a letter. The second argument, if provided,
is ignored as soon as the first one begins with a letter; if only one numeric
argument is provided, the column number is assumed to be 0.

The two following instructions are equivalent and return the second cell of the
second row in a table (assuming that ``t`` is a previously selected table)::

   c = t.get_cell('B2')
   c = t.get_cell(1, 1)

``get_row()`` allows the user to select a table row as an ODF element. This
method requires a zero-based numeric value.

``get_column()`` works according to the same logic and returns a table column
ODF element.

The full set of row and column objects may be selected using the table-based
``get_rows()`` and ``get_columns()`` methods. By default these methods
return repectively the full list of rows or columns. They can be restricted to
a specified range of rows or columns. The restriction may be expressed through
two numeric, zero-based arguments indicating the positions of the first and the
last item of the range. Alternatively, the range may be specified using a more
"spreadsheet-like" syntax, in only one alphanumeric argument representing the
visible representation of the range through a GUI; this argument is the
concatenation of the visible numbers of the starting and ending elements,
separated by a ":", knowing that "1" is the visible number of the row zero
while "A" is the visible number or the column zero. As a consequence, the two
following instructions are equivalent and return a list including the rows from
5 to 10 belonging to the table ``t``::

   rows = t.get_rows(5, 10)
   rows = t.get_rows('6:11')

According to the same logic, each of the two instruction below returns the
columns from 8 to 15::

   cols = t.get_columns(8, 15)
   cols = t.get_columns('I:P')

Once selected, knowing that cells are contained in rows, a row-based
``get_cell()`` method is provided. When called from a row object,
``get_cell()`` requires the same parameter as the table-based ``get_column()``
method. For example, the following sequence returns the same cell as in the
previous example::

   r = t.get_row(1)
   c = r.get_cell(1)

Cell range selection
--------------------

``get_cells()`` can extract rectangular ranges of cells in order to allow the
applications to store and process them out of the document tree, through
regular 2D tables. The range selection is defined by the coordinates of the
top left and the bottom right cells of the target area. The selection is
done using the table-based ``get_cells()`` method, with two possible syntaxes,
i.e. the spreadsheet-like one and the numeric one. The first one requires an
alphanumeric argument whose first character is a letter and that includes a
':', while the second one requires four numeric arguments. As an example, the
two following instructions, which are equivalent, return a bi-dimensional array
corresponding to the cells of the ``B2:D15`` area of a table::

   cells = t.get_cells("B2:D15")
   cells = t.get_cells(1,1,14,3)

Note that, after such a selection, ``cells[0,0]`` contains the "B2" cell of
the ODF table.

If ``get_cells()`` is called without argument, the selection covers the whole
table.

A row object has its own ``get_cell()`` method. The row based version of
``get_cells()`` returns, of course, a one-row table of cell objects. When
used without argument, it selects all the cells of the row. It may be called
with either a pair of numeric arguments that represent the start and the end
positions of the cell range, or an alphanumeric argument (whose the numeric
content is ignored and should be omitted) corresponding to the start and end
columns in conventional spreadsheet notation. The following example shows two
ways to select the same cell range (beginning at the 2nd position and ending
at the 26th one) in a previously selected row::

   cells = r.get_cells('B:Z')
   cells = r.get_cells(1, 25)

**Note**: The range selection feature provided by the level 1 API is a
building block for the lpOD level 2 business-oriented cell range objects.

Row and column customization
----------------------------

The objects returned by ``get_row()`` and ``get_column()`` can be customized
using the standard ``set_attribute()`` or ``set_attributes()`` method. Possible
attributes are:

- ``style``: the name of the applicable style (which should be at display time
  a valid row or column style);
- ``default cell style name``: the default style which apply to each cell in
  the column or row unless this cell has no defined style attribute;
- ``visibility``: specifies the visibility of the row or column; legal values
  are ``visible``, ``collapse`` and ``filter``.

Table expansion
---------------

A table may be expanded vertically and horizontally, using its ``add_row()`` and
``add_column()`` methods.

``add_row()`` allows the user to insert one or more rows at a given position in
the table. The new rows are copies of an existing one. Without argument, a
single row is just appended as the end. A ``number`` named parameter provides
the number of rows to insert.

An optional ``before`` named parameter may be provided; if defined, the value
of this parameter must be a row number (in numeric, zero-based form) in the
range of the table; the new rows are created as clones of the row existing at
the given position then inserted at this position, i.e. *before* the original
reference row. A ``after`` parameter may be provided instead of ``before``;
it produces a similar result, but the new rows are inserted *after* the
reference row. Note that the two following instructions produce the same
result::

   t.add_row(number=1, after=-1)
   t.add_row()

The inserted rows are initialized as clones of the row used as the reference
through the ``after`` or ``before`` or of the last existing row if the new
row in appended at the end. So the new rows (and their cells) inherit the same
style and content as an existing one.

The ``add_column()`` method does the same thing with columns as ``add_row()``
for rows. However, because the cells belong to rows, it works according to a
very different logic. ``add_column()`` inserts new column objects (clones of an
existing column), then it goes through all the rows and inserts new cells
(cloning the cell located at the reference position) in each one.

Of course, it's possible to use ``insert_element()`` in order to insert a row,
a column or a cell externally created (or extracted from an other table from
another document), provided that the user carefully checks the consistency of
the resulting contruct. As an example, the following sequence appends a copy
of the first row of ``t1``after the 5th row of ``t2``::

   to_be_inserted = t1.get_row(0).clone();
   t2.insert_element(to_be_inserted, after=t2.get_row(5))

Row and column group handling
-----------------------------

The content expansion and content selection methods above work with the table
body. However it's possible to manage groups of rows or columns. A group may
be created with existing adjacent rows or columns, using ``set_row_group()``
and ``set_column_group()`` respectively. These methods take two mandatory
arguments, which are the numeric positions of the starting and ending elements
of the group. In addition, an optional ``display`` named boolean parameter
may be provided (default=true), instructing the applications about the
visibility of the group.

Both ``set_row_group()`` and ``set_column_group()`` return an object which can
be used later as a context object for any row, column or cell retrieval or
processing. An existing group may be retrieved according to its numeric
position using ``get_row_group()`` or ``get_column_group()`` with the position
as argument, or without argument to get the first (or the only one) group.

A group can't bring a particular style; it's just visible or not. Once created,
its visibility may be turned on and off by changing its ``display`` value
through ``set_attribute()``.

A row group provides a ``add_row()`` method, while a column group provides a
``add_column()`` method. These methods work like their table-based versions,
and they allow the user to expand the content of a particular group.

A group can contain a *header* (see below).

Table headers
-------------

One or more rows or columns in the beginning of a table may be organized as
a *header*. Row and columns headers are created using the ``set_row_header()``
and ``set_column_header()`` table-based methods, and retrieved using
``get_row_header()`` and ``get_column_header()``. A row header object brings its
own ``add_row()`` method, which works like the table-based ``add_row()`` but
appends the new rows in the space of the row header. The same logic applies to
column headers which have a ``add_column()`` method. An optional positive
integer argument may specify the number or rows or columns to include in the
header (default=1).

A table can't directly contain more than one row header and one column header.
However, a column group can contain a column header, while a row group can
contain a row header. So the header-focused methods above work with groups as
well as with tables.

A table header doesn't bring particular properties; it's just a construct
allowing the author to designate rows and columns that should be automatically
repeated on every page if the table doesn't fit on a single page.

The ``get_xxx()`` table-based retrieval methods ignore the content of the
headers. However, it's always possible to select a header, then to used it as
the context object to select an object using its coordinates inside the header.
For example, the first instruction below gets the first cell of a table body,
while the third and third instructions select the first cell of a table header::

   c1 = table.get_cell(0,0)
   header = table.get_header()
   c2 = header.get_cell(0,0)

Individual cell property handling
---------------------------------
A cell owns both a *content* and some *properties* which may be processed
separately.

The cell content is a list of one or more ODF elements. While this content is
generally made of a single paragraph, it may contain several paragraphs and
various other objects. The user can attach any content element to a cell using
the standard ``insert_element()`` method. However, for the simplest (and the
most usual) cases, it's possible to use ``set_text()``. The cell-based
``set_text()`` method diffs from the level 0 ``set_text()``: it removes the
previous content elements, if any, then creates a single paragraph with the
given text as the new content. In addition, this method accepts an optional
``style`` named parameter, allowing the user to set a paragraph style for the
new content. To insert more content (i.e. additional paragraphs and/or other
ODF elements), the needed objects have to be created externally and attached
to the cell using ``insert_element()``. Alternatively, it's possible to remove
the existing content (if any) and attach a full set of content elements in a
single instruction using ``set_content()``; this last cell method takes a list
of arbitrary ODF elements and appends them (in the given order) as the new
content.

The ``get_content()`` cell method returns all the content elements as a list.
For the simplest cases, the cell-based ``get_text()`` method directly returns
the text content as a flat string, without any structural information and
whatever the number and the type of the content elements.

The cell properties may be read or changes using ``get_xxx()`` and ``set_xxx()``
methods, where ``xxx`` stands for one of the following:

- ``style``: the name of the cell style;
- ``type``: the cell value type, which may be one of the ODF supported data
   types, used when the cell have to contain a computable value (omitted with
   text cells);
- ``value``: the numeric computable value of the cell, used when the ``type`` is
   defined;
- ``currency``: the international standard currency unit identifier (ex: EUR,
   USD), used when the ``type`` is ``currency``;
- ``formula``: a calculation formula whose result is a computable value (the
   grammar and syntax of the formula is application-specific and not ckecked
   by the lpOD API (it's stored as flat text and not interpreted);
- ``protect``: boolean (default false), tells the applications that the cell
   can't be edited.

If ``set_currency`` is used with a non-null value, then the ``type`` of the
cell is automatically set to ``currency``. If ``set_type`` forces a type that
is not ``currency``, then the cell currency is set to none.

Cell span extension
-------------------

A cell may be expanded in so it covers one or more adjacent columns and/or rows.
The cell-based ``set_span()`` method allows the user to control this expansion.
It takes ``rows`` and ``columns`` as parameters, specifying the number of rows
and the number of columns covered. The following example selects the "B4" cell
then expands it over 4 columns and 3 rows::

   cell = table.get_cell('B4')
   cell.set_span(rows=3, columns=4)

The existing span of a cell may be get using ``get_span()``, which returns the
``rows`` and ``columns`` values.

This method changes the previous span of the cell. The default value for each
parameter is 1, so a ``set_span()`` without argument reduces the cell at its
minimal span.

When a cell is covered due to the span of another cell, it remains present and
holds its content and properties. However, it's possible to know at any time if
a given cell is covered or not through the boolean ``is_covered()`` cell method.
In addition, the span values of a covered cell are automatically set to 1, and
``set_span()`` is forbidden with covered cells.

Note that the API doesn't support cell spans that spread across table header
or group boundaries.

