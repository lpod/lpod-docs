# -*- coding: UTF-8 -*-
#
# Copyright (c) 2009 Ars Aperta, Itaapy, Pierlis, Talend.
#
# Authors: David Versmisse <david.versmisse@itaapy.com>
#          Hervé Cauwelier <herve@itaapy.com>
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

# Import from the Standard Library
from glob import glob

# Import from lpod
from lpod.document import odf_new_document_from_type
from lpod.frame import odf_create_image_frame
from lpod.paragraph import odf_create_paragraph
from lpod.table import import_from_csv, odf_create_column

# Get elements
document = odf_new_document_from_type('spreadsheet')
body = document.get_body()

for id, filename in enumerate(glob('./files/*.csv')):
    table = import_from_csv(filename, u'Table %s' % (id + 1))

    # Some information
    width = table.get_table_width()
    height = table.get_table_height()

    # Remove empty rows and cells on the edge
    table.rstrip_table()

    # Accessing rows
    first_row = table.get_row(0)
    first_row.set_row_style(u"Another style")

    # Accessing cells from the row
    first_cell = first_row.get_cell(0)

    # Change a cell easily from a Python type
    first_cell.set_cell_value(u"Hello")

    # Modified cells must be pushed back
    # Could be pushed to another position
    first_row.set_cell(0, first_cell)

    # Modified rows must be pushed back
    # Could be pushed to another position
    table.set_row(0, first_row)

    # Accessing cells from the table
    second_cell = table.get_cell("B1")

    # Cells are XML elements
    second_cell.clear()
    second_cell.append_element(odf_create_paragraph(u"World"))

    # Modified cells must be pushed back
    # Could be pushed to another position
    table.set_cell((1, 0), second_cell)

    # Append a column (and adjust the table size)
    table.append_column(odf_create_column())

    # Add an image in the document
    image_uri = document.add_file('../.static/banner-lpod_en.png')

    # Images are in frame
    frame = odf_create_image_frame(image_uri, size=('11.87cm', '1.75cm'),
            position=('0cm', '0cm'))

    # Displaying an image in a cell is tricky: the document type must be
    # given or the table attached to the document
    table.set_cell_image((-1, 0), frame, type=document.get_type())

    # The table is a regular element
    body.append_element(table)

# Save
filename = 'spreadsheet.ods'
document.save(filename, pretty=True)
print 'Document "%s" generated.' % filename
