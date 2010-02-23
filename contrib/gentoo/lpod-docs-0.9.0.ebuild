# Copyright 1999-2010 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

DESCRIPTION="Languages and Plateforms OpenDocument : Documentation"
HOMEPAGE="http://docs.lpod-project.org"
SRC_URI="http://download.lpod-project.org/${PN}/${P}.tgz"

LICENSE="GPL"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE=""

DEPEND=""
RDEPEND=""

src_install(){
	insinto /usr/share/doc/${PN}/
	cp -R "${S}/" "${D}/usr/share/doc/${PN}/" || die "Installation falied!"
}

pkg_postinst(){
	einfo ""
	einfo "Lpod Documentation installed into :"
	einfo "/usr/share/doc/${PN}/${P}"
	einfo "----"
	einfo "On line documentation :"
	einfo "${HOMEPAGE}"
	einfo ""
	einfo ""
}
