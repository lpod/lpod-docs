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

- ``note_class`` or ``class``: the class option (default=footnote);
- ``citation``: the citation mark (i.e. the text string that should be displayed
  by editing/viewing applications at the place where the note is referred to);
- ``body``: the content of the note, provided as a list of paragraphs previously
  created;
- ``text``: the content of the note, provided as a flat character string;
- ``style``: the name of the paragraph style for the content of the note.

The ``text`` and ``style`` parameters are ignored if ``body`` is provided,
because ``body`` is supposed to be a list of one or more paragraphs, each one
with its own style and content. The ``body`` option allows the applications to
reuse an existing content for one or more notes in one or more documents.

It's possible to create a note as a free element, so it can be later inserted
in place (and replicated for reuse in several locations in one or more
documents), using general purpose insertion methods such as
``insert_element()``.

By default, ``set_note()`` inserts the new note at the beginning (i.e. as the
first child element) of the calling element. However, it's possible to specify
another position within the text content of the element, using the same
positioning options as the ``set_bookmark()`` method, namely ``position``,
``before``, ``after``, and so on (see ``set_bookmark()`` in the "Text bookmarks"
section of "Text marks and indices").

Regarding the identifier, the user can provide either an explicit value, or an
function that is supposed to return an automatically generated unique value. If
the class option is missing, the API automatically selects 'footnote'.

Footnote and endnote content
-----------------------------

A note is a container whose body can be filled with one or more paragraphs or
item lists at any time, before or after the insertion in the document. As a
consequence, a note can be used as a regular context for paragraph or list
appending or retrieval operations.

Note that neither the OpenDocument schema nor the lpOD level 1 API prevents the
user from including notes into a note body; however the lpOD team doesn't
recommend such a practice.

Annotation creation [tbc]
-------------------------

Annotations don't have identifiers and are directly linked to a given offset in
a given text container.

Change tracking [todo]
----------------------


