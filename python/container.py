# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Itaapy, ArsAperta, Pierlis, Talend

# Import from the Standard Library
from copy import deepcopy
from zipfile import ZipFile

# Import from itools
from itools import vfs
from itools.core import get_abspath
from itools.xml import XMLParser, get_element


# Classes and their default template
ODF_CLASSES = {
        'text': 'templates/text.ott',
        'spreadsheet': 'templates/spreadsheet.ots',
        'presentation': 'templates/presentation.otp',
        'drawing': 'templates/drawing.otg',
        # TODO
}


# File extensions and their mimetype
ODF_EXTENSIONS = {
        'odt': 'application/vnd.oasis.opendocument.text',
        'ott': 'application/vnd.oasis.opendocument.text-template',
        'ods': 'application/vnd.oasis.opendocument.spreadsheet',
        'ots': 'application/vnd.oasis.opendocument.spreadsheet-template',
        'odp': 'application/vnd.oasis.opendocument.presentation',
        'otp': 'application/vnd.oasis.opendocument.presentation-template',
        'odg': 'application/vnd.oasis.opendocument.graphics',
        'otg': 'application/vnd.oasis.opendocument.graphics-template'
}


# Mimetypes and their file extension
ODF_MIMETYPES = {
        'application/vnd.oasis.opendocument.text': 'odt',
        'application/vnd.oasis.opendocument.text-template': 'ott',
        'application/vnd.oasis.opendocument.spreadsheet': 'ods',
        'application/vnd.oasis.opendocument.spreadsheet-template': 'ots',
        'application/vnd.oasis.opendocument.presentation': 'odp',
        'application/vnd.oasis.opendocument.presentation-template': 'otp',
        'application/vnd.oasis.opendocument.graphics': 'odg',
        'application/vnd.oasis.opendocument.graphics-template': 'otg',
        # XML-only document
        'application/xml': 'xml',
}


# Standard parts in the container (other are regular paths)
ODF_PARTS = ['content', 'meta', 'mimetype', 'settings', 'styles']


class odf_container(object):
    """Representation of the ODF document.
    """

    def __init__(self, uri):
        if not vfs.exists(uri):
            raise ValueError, "URI is not found"
        if not vfs.can_read(uri):
            raise ValueError, "URI is not readable"
        if vfs.is_folder(uri):
            raise NotImplementedError, ("reading uncompressed ODF "
                                        "is not supported")

        mimetype = vfs.get_mimetype(uri)
        if not mimetype in ODF_MIMETYPES:
            raise ValueError, "mimetype '%s' is unknown" % mimetype

        self.uri = uri
        self.mimetype = mimetype
        self.file = vfs.open(uri)


    def clone(self):
        clone = object.__new__(self.__class__)
        for name in self.__dict__:
            if name in ('uri', 'file'):
                setattr(clone, name, None)
            else:
                value = getattr(self, name)
                value = deepcopy(value)
                setattr(clone, name, value)

        return clone


    def __get_part_xml(self, part_name):
        if part_name not in ODF_PARTS:
            raise ValueError, ("Third-party parts are not supported "
                               "in an XML-only ODF document")
        if part_name == 'mimetype':
            part = self.mimetype
        else:
            events = XMLParser(self.file.read())
            element = get_element(list(events),
                                  'document-%s' % part_name)
            part = list(element.get_content_elements())
        return part



    def __get_part_zip(self, part_name):
        archive = ZipFile(self.file)
        if part_name in ODF_PARTS and part_name != 'mimetype':
            data = archive.read('%s.xml' % part_name)
            part = list(XMLParser(data))
        else:
            part = archive.read(part_name)
        archive.close()
        return part


    def get_part(self, part_name):
        if self.mimetype == 'application/xml':
            return self.__get_part_xml(part_name)
        else:
            return self.__get_part_zip(part_name)



def new_odf_container(odf_class=None, template_uri=None):
    """Return an "odf_container" instance of a new ODF document, from a
    default template or from the given template.
    """
    if ((odf_class is None and template_uri is None)
         or (odf_class is not None and template_uri is not None)):
        raise ValueError, "either 'odf_class' or 'template_uri' is mandatory"
    if odf_class not in ODF_CLASSES:
        raise ValueError, "unknown ODF class '%s'" % odf_class

    if odf_class is not None:
        template_path = ODF_CLASSES[odf_class]
        template_uri = get_abspath(template_path)

    template = get_odf_container(template_uri)

    # Return a copy of the template
    return template.clone()



def get_odf_container(uri):
    """Return an "odf_container" instance of the ODF document stored at the
    given URI.
    """
    return odf_container(uri)
