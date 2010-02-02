# -*- coding: UTF-8 -*-
#
# Copyright (c) 2009 Ars Aperta, Itaapy, Pierlis, Talend.
#
# Authors: David Versmisse <david.versmisse@itaapy.com>
#          Hervé Cauwelier <herve@itaapy.com>
#          Luis Belmar-Letelier <luis@itaapy.com>
#          Romain Gauthier <romain@itaapy.com>
#
# This file is part of Lpod (see: http://lpod-project.org).
# Lpod is free software; you can redistribute it and/or modify it under
# the terms of either:
#
# a) the GNU General Public License as published by the Free Software
#    Foundation, either version 3 of the License, or (at your option)
#    any later version.
#    Lpod is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with Lpod.  If not, see <http://www.gnu.org/licenses/>.
#
# b) the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#

# Import from lpod
from lpod.document import odf_new_document_from_type, odf_get_document
from lpod.heading import odf_create_heading
from lpod.list import odf_create_list, odf_create_list_item
from lpod.note import odf_create_note, odf_create_annotation
from lpod.paragraph import odf_create_paragraph
from lpod.table import odf_create_table
from lpod.toc import odf_create_toc

# Creation of the document
document = odf_new_document_from_type('text')
body = document.get_body()

# Add (empty) Table of content
toc = odf_create_toc()
body.append_element(toc)

# Add Paragraph
paragraph = odf_create_paragraph(u'lpOD generated Document')
body.append_element(paragraph)

# Add Heading
heading = odf_create_heading(1, text=u'Lists')
body.append_element(heading)

#
# A list
#
my_list = odf_create_list([u'chocolat', u'café'])

item = odf_create_list_item(u'Du thé')
item.append_element(odf_create_list([u'thé vert', u'thé rouge']))
my_list.append_item(item)

# insert item by position
my_list.insert_item(u'Chicorée', position=1)

# insert item by relative position
the = my_list.get_item_by_content(u'thé')
my_list.insert_item(u'Chicorée', before=the)
my_list.insert_item(u'Chicorée', after=the)

body.append_element(my_list)

#
# Footnote with odf_create_note of class "footnote" and insert_note
#
body.append_element(odf_create_heading(1, u"Footnotes"))
paragraph = odf_create_paragraph(u'A paragraph with a footnote '
                                      u'about references in it.')
note = odf_create_note(note_id='note1', citation=u"1",
                       body=u'Author, A. (2007). "How to cite references", '
                            u'New York: McGraw-Hill.')
paragraph.insert_note(note, after=u"graph")
body.append_element(paragraph)

#
# Annotations
#
body.append_element(odf_create_heading(1, u"Annotations"))
paragraph = odf_create_paragraph(u"A paragraph with an annotation "
                                 u"in the middle.")
annotation = odf_create_annotation(u"It's so easy!", creator=u"Luis")
paragraph.insert_annotation(annotation, after=u"annotation")
body.append_element(paragraph)

#
# Tables
#
body.append_element(odf_create_heading(1, u"Tables"))
body.append_element(odf_create_paragraph(u"A table:"))
table = odf_create_table(u"Table 1", width=3, height=3)
body.append_element(table)

#
# Applying styles
#
body.append_element(odf_create_heading(1, u"Applying Styles"))

# Copying a style from another document
lpod_styles = odf_get_document('../../python/templates/lpod_styles.odt')
highlight = lpod_styles.get_style('text', u"Yellow Highlight",
                                  display_name=True)
assert highlight is not None
document.insert_style(highlight)

# Apply this style to a pattern
paragraph = odf_create_paragraph(u'Highlighting the word "highlight".')
paragraph.set_span(highlight, u"highlight")
body.append_element(paragraph)

# Fill the TOC
toc.toc_fill()


# Save
filename = 'text.odt'
document.save(filename, pretty=True)
print 'Document "%s" generated.' % filename
