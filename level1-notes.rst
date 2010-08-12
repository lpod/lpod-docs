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


Notes
=========

.. contents::
   :local:

Generally speaking, a note is an object whose main function is to allow the user
to set some text content out of the main document body but to structurally
associate this content to a specific location in the document body. The content
of a note is stored in a sequence of one or more paragraphs and/or item lists.

The lpOD API supports four kinds of notes, so-called footnotes, endnotes,
annotations and change marks. Footnotes and endnotes have the same structure
and differ only by their display location in the document body. Annotations are
specific objects, that don't apparently belong to the document content but that
allow the users to associate persistent information to the content.

Footnote and endnote creation
-----------------------------

These notes are created in place using the element-based ``set_note()`` method,
that requires a note identifier (unique for the document) as its first argument,
and the following note-specific parameters:

- ``class`` or ``note_class``: the class option, whose default is ``footnote``
  (``note_class`` is used with programming languages that don't allow ``class``
  as a parameter name);
- ``citation``: the citation mark (i.e. a formatted string representing the
  sequence number, see "Note citation" in ODF 1.1 §5.3.1);
- ``label``: the optional text label that should be displayed at the insertion
  point of the note; if this parameter is omitted, the displayed note label will
  be an automatic sequence number;
- ``body``: the content of the note, provided either as a list of one or more
  previously created ODF content elements (preferently paragraphs), or as an
  already available note body element (produced, for example, by cloning the
  body of another note);
- ``text``: the content of the note, provided as a flat character string;
- ``style``: the name of the paragraph style for the content of the note.

The ``text`` and ``style`` parameters are ignored if ``body`` is provided,
because ``body`` is supposed to be a list of one or more paragraphs, each one
with its own style and content. The ``body`` option allows the applications to
reuse an existing content for one or more notes in one or more documents.
Without the ``body`` parameter, a paragraph is automatically created and filled
with the value of ``text``. If neither ``body`` nor ``text`` is provided, the
note is created with an empty paragraph.

The list of ODF elements provided through the ``body`` parameter may contain
almost any content object; neither the OpenDocument schema nor the lpOD level 1
API prevents the user from including notes into a note body; however the lpOD
team doesn't recommend such a practice.

It's possible to create a note as a free element with the ``odf_create_note``
constructor, so it can be later inserted in place (and replicated for reuse in
several locations in one or more documents), using general purpose insertion
methods such as ``insert_element()``.

By default, ``set_note()`` inserts the new note at the beginning (i.e. as the
first child element) of the calling element. However, it's possible to specify
another position within the text content of the element, using the same
positioning options as the ``set_bookmark()`` method, namely ``position``,
``before``, ``after``, and so on (see ``set_bookmark()`` in the "Text bookmarks"
section of "Text marks and indices").

As an example, the following instruction inserts a footnote whose citation mark
is an asterisk, with a given text content, immediately after the "xyz" substring
in a paragraph::

  paragraph.set_note(
    "note0004",
    note_class = "footnote",
    after = "xyz",
    label ="*",
    text = "The footnote content",
    style = "Note body"
    )
    
``set_note()`` returns the newly created object, that is available for later
use.

Footnote and endnote retrieval
------------------------------

Once set somewhere in a document, a note may be retrieved the context-based
``get_note()`` method, with the note identifier as argument.

It's possible to extract a list of notes using the context-based
``get_notes()``. Without argument, this method returns all the notes of the
context. However, it's possible to provide the ``note_class``, ``citation``,
and/or ``label`` parameters in order to select the notes that match them. The
following example extract the endnotes whose citation mark is "5" in a given
section::

  end_notes = section.get_notes(
    note_class = "endnote",
    citation = "1"
    )

This method may allow the users to retrieve a note without knowledge of its
identifier.

Footnote and endnote methods
-----------------------------

Read accessors
~~~~~~~~~~~~~~

get_id()
    the note identifier (generic element method).

get_class()
    the note class.

get_citation()
    the note citation.

get_label()
    the note label.

get_body()
    the root of the note body, as a single container; this object may be used
    as a context element for appending or removing any object in the note body;
    the real content is made of the children elements of the body; it may be
    cloned in order to be reused as the body of another note in the same
    document or elsewhere.

Write accessors
~~~~~~~~~~~~~~~

set_id(new_id)
    changes the identifier (generic element method); be careful, ``set_id()``
    with a null value erases the identifier (but, with a defined value, allows
    to restore it at any time).

set_class(footnote|endnote)
    allows to turn a footnote into a endnote or vice versa.

set_citation()
    changes the note citation mark.

set_label(new_label)
    changes the note label.

set_body()
    takes the same kinds of content as the ``body`` parameter of ``set_note()``;
    provides the note with a new body; any previous content is deleted and
    replaced; if ``set_body()`` is used without argument or with a null value,
    the previous content is replaced by a single empty paragraph.


Annotation creation
-------------------

An annotation is particular note that has neither identifier nor citation
mark, but which may be put like a footnote or a endnote at a given offset in a
given text container. On the other hand, it stores a date and an author's name.

Annotations are created using ``set_annotation()``, that takes the same
positioning parameters as ``set_note()`` and ``set_bookmark()``, and the
following other parameters:

- ``date``: the date/time of the annotation (ISO-8601 format); if this
  parameter is omitted, the current system date applies by default;

- ``author``: the name of the author of the annotation (which may be an
  arbitrary application-provided string); if this parameter is omitted, lpOD
  tries to set it to the user name of the process owner and, if such an
  information is not available in the runtime environment, the annotation
  is created with an empty string as the author name (not recommended);

- ``content``: a list of one or more regular text paragraphs that will become
  the content of the annotation (beware, unlike ``set_note()``,
  ``set_annotation()`` requires a list of paragraphs and doesn't accept a
  previously existing note body or other non-paragraphs ODF objects);

- ``text``: like with ``set_note()`` (ignored if ``body`` is provided);

- ``style``: like with ``set_note()`` (ignored if ``body`` is provided).

``set_annotation()`` returns the newly created object, that is available for
later use.


Annotation retrieval
--------------------

Annotations may be selected is through the context-based ``get_annotations()``
method that takes ``date`` and ``author`` as optional parameters.

Without parameter, this method returns the full list of the annotations that
appear in the context. The use of one or two of the optional parameters allows
to restrict the list according to the given ``date`` and/or ``author``.

While a typical human writer using an interactive editing application should
never be able to put two annotations in the same time in the same document,
an automatic document processing application can do that. So the date/author
combination should not be regarded as an absolute identifier; as a
consequence, ``get_annotations()`` always returns a list (possibly containing
a single paragraph or nothing).

Annotation methods
------------------

Read accessors
~~~~~~~~~~~~~~

get_date()
    returns the stored date.

get_author()
    returns the stored author's name.

get_content()
    returns the content as a list of paragraph(s).

Write accessors
~~~~~~~~~~~~~~~

set_date(new_date)
    changes the stored date; without arguments, the current date applies.

set_author()
    changes the stored author's name; without argument, the process owner
    applies.

set_content()
    replaces the current content using the argument, that is a list of one
    or more paragraphs.

An annotation object may be used as a regular context element in order to
change its content through generic context-based element insertion, deletion of
updating methods. No particular check is done, so the user should ensure that
inserted elements are always paragraphs.


Tracked change retrieval
------------------------

lpOD applications can retrieve all the change tracking data which may have been
stored in text documents by ODF-compliant editors. On the other hand, lpOD
doesn't provide any automatic tracking of the changes made by lpOD-based
applications.

A tracked change may be retrieved in a document using the ``get_change()`` and
``get_changes()`` document-based methods.

Every tracked change is stored as a ODF change object that owns the following
attributes:

- ``id``: the identifier of the tracked change (unique for the document);
- ``date``: the date/time of the change (ISO-8601 format);
- ``author``: the name of the user who made the change.

An change may be individually retrieved using ``get_change()`` with a change
identifier as argument.

The ``get_changes()`` method, without argument, returns the full list of
tracked changes. The list may be filtered according to ``date`` and/or
``author`` optional parameters.

If a single date is provided as the ``date`` parameter, then the result set
contains only tracked change elements that exactly match it, if any. However
the user may specify a time interval by providing a list of two dates as the
``date`` parameter; so any tracked change whose date belongs to the given
interval is candidate. An empty string, or a 0 value, is allowed as start or
end date, meaning that there is no inferior or superior limit.

``get_changes()`` returns only the tracked changes whose author exactly matches
the given ``author`` parameter, if this parameter is set.

The document-based ``get_change()`` and ``get_changes()`` methods look for
tracked changes in the document ``content`` part only, and works with text
documents only.

In addition, lpOD provides ``get_change()`` and ``get_changes()`` as context
methods, allowing the applications to call them from any arbitrary element, so
the search is directed and restricted to a particular context. If the calling
element is not able to track the changes, these methods always return nothing
but they are neutral. If the calling element contains tracked changes, they
work like their document-based versions in the given context. This feature
allows the users to retrieve tracked changes in page headers and footers,
knowing that these changes are registered in the contexts of the corresponding
page style definitions, and not in the document content. 

Tracked change methods
----------------------

Each individual tracked change object, previously selected, own the following
methods:

delete()
    deletes the tracked change, i.e. removes any persistent information about
    the tracked change object from the document.

get_id()
    returns the identifier.

get_date()
    returns the date.

get_author()
    returns the author's name.
  
get_type()
    returns the type of change, that is either ``insertion`` or ``deletion``.

get_deleted_content()
    returns the content of the deleted content as a list of ODF elements, if
    the change type is ``deletion`` (and returns a null value otherwise).

get_change_mark()
    returns the position mark of the change; if the change type is ``deletion``,
    this object is located at the place of the deleted content; if the change
    type is ``insertion``, it's located at the beginning of the inserted
    content.

get_deletion_mark()
    if the change type is ``deletion``, returns the position mark element that
    indicates the place of the deleted content; returns nothing if the change
    type is not ``deletion``.

get_insertion_marks()
    if the change type is ``insertion``, returns a pair of position mark
    elements, respectively located at the beginning and at the end of the
    inserted content (this pair of elements may be used in a similar way as
    the start and end elements of a range bookmark, in order to determine the
    limits of the inserted content); it returns nothing if the change type is
    ``deletion``.




