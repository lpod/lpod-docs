lpod documentation
==================

Lpod is a library implementing the ISO/IEC 26300 OpenDocument Format standard (ODF)


Build the doc
-------------

Before attempting to build the documentation, you should::

- install the python part of the lpOD project[1].
- install Sphinx http://sphinx.pocoo.org
- install texlive http://www.tug.org/texlive/

Makefile
---------
::

  luis@spinoza ~/lpod/sandbox/lpod/doc $ make
  Please use `make <target>' where <target> is one of
    html      to make standalone HTML files
    latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter
    pdf       to make PDF files, you can set PAPER=a4 or PAPER=letter
    changes   to make an overview over all changed/added/deprecated items
    linkcheck to check all external links for integrity
    release   to make html/pdf and store the files in two tar.gz
