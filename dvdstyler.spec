%define		oname	DVDStyler
%define		prerel	rc1

Name:		dvdstyler
Summary:	DVD authoring application
Version:	2.3
Release:	%{?preprel:0.%{prerel}.}1
Epoch:		1
Source0:	http://downloads.sourceforge.net/project/dvdstyler/%{name}%{?prerel:-devel}/-%{version}%{?prerel}/%{oname}-%{version}%{?prerel}.tar.bz2
Patch1:		DVDStyler-2.1-ljpeg.patch
URL:		http://dvdstyler.sourceforge.net/
License:	GPLv2+
Group:		Video
BuildRequires:	imagemagick
BuildRequires:	wxsvg-devel >= 1.1.9
BuildRequires:	wxgtku2.8-devel
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	dvdauthor >= 0.7.0
BuildRequires:	netpbm
BuildRequires:	dvd+rw-tools
BuildRequires:	mkisofs
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
Buildrequires:	libexif-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	xmlto
BuildRequires:	zip
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	ffmpeg
Requires:	dvdauthor
Requires:	mjpegtools
Requires:	dvd+rw-tools
Requires:	mkisofs

%description
DVDstyler is a DVD authoring program. The main DVDStyler features are:
    * you can drag and drop MPEG files directly
    * you can import image file for background
    * you can create NTSC/PAL menu
    * you can place text and images anywhere on the menu screen
    * you can change font/color
    * you can put basic text buttons, change font/color and background color
    * you can set chapters for each movie
    * you can change post command for each movie

%prep
%setup -q -n %{oname}-%{version}%{?prerel}
%patch1 -p1
#fix desktop file
%__sed -i -e 's,%{name}.png,%{name},g' data/dvdstyler.desktop

%build
%configure2_5x --with-wx-config=%{_bindir}/wx-config-unicode
%make

%install
%makeinstall_std
%__rm -fr %{buildroot}%{_docdir}

desktop-file-install --vendor='' \
	--dir=%{buildroot}%{_datadir}/applications \
	--remove-category='Application' \
	--add-category='Video;AudioVideoEditing' \
	%{buildroot}%{_datadir}/applications/*.desktop

%__mkdir_p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -size 48x48 src/rc/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -size 32x32 src/rc/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -size 16x16 src/rc/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

#remove duplicate files
%__rm -fr %{buildroot}%{_libdir}/share/doc/dvdstyler/

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png


%changelog
* Tue Jul 03 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1:2.3-1
+ Revision: 807983
- update to 2.3rc1

* Thu Jan 12 2012 Andrey Bondrov <abondrov@mandriva.org> 1:2.1-1
+ Revision: 760390
- New version 2.1, switch to utf8 wxGTK2.8

* Thu Nov 18 2010 Funda Wang <fwang@mandriva.org> 1:1.8.1-1mdv2011.0
+ Revision: 598722
- BR flex
- BR bison
- update to new version 1.8.1

* Mon Apr 26 2010 Emmanuel Andry <eandry@mandriva.org> 1:1.8.0.2-1mdv2010.1
+ Revision: 539312
- New version 1.8.0.2
- drop p0 (no more needed)

* Sat Jan 16 2010 Funda Wang <fwang@mandriva.org> 1:1.7.4-2mdv2010.1
+ Revision: 492234
- rebuild for new libjpegv8

* Sun Dec 27 2009 Ahmad Samir <ahmadsamir@mandriva.org> 1:1.7.4-1mdv2010.1
+ Revision: 482719
- update to 1.7.4 (use 1.7.4_3 tarball since 1.7.4 doesn't build)

* Sun Aug 23 2009 Funda Wang <fwang@mandriva.org> 1:1.7.3-2mdv2010.0
+ Revision: 419745
- rebuild for new libjpeg v7

* Mon Aug 17 2009 Frederik Himpe <fhimpe@mandriva.org> 1:1.7.3-1mdv2010.0
+ Revision: 417215
- Update to new version 1.7.3

* Sat Mar 07 2009 Emmanuel Andry <eandry@mandriva.org> 1:1.7.2-1mdv2009.1
+ Revision: 352406
- BR zip

  + Funda Wang <fwang@mandriva.org>
    - New version 1.7.2

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Fri Dec 05 2008 Götz Waschk <waschk@mandriva.org> 1:1.7.1-1mdv2009.1
+ Revision: 310625
- new version
- bump deps
- drop useless build deps

  + Adam Williamson <awilliamson@mandriva.org>
    - rebuild for new ffmpeg

* Sat Sep 06 2008 Adam Williamson <awilliamson@mandriva.org> 1:1.7.0-1mdv2009.0
+ Revision: 281891
- package man page
- drop netpbm and mpgtx requires (per upstream, no longer needed)
- drop ffmpeg.patch: no longer needed
- new release 1.7.0

* Sat Jun 14 2008 Adam Williamson <awilliamson@mandriva.org> 1:1.6.2-1mdv2009.0
+ Revision: 219092
- add ffmpeg.patch - fix ffmpeg detection and usage for MDV's layout
- fix genisoimage.patch - it got messed up over last two changes by fwang and aginies
- now br ffmpeg-devel
- clean spec
- misc spec cleanups
- drop legacy icons
- new license policy

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Antoine Ginies <aginies@mandriva.com>
    - add libexif-devel buildrequires
    - new release
    - new version
    - new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Aug 27 2007 Funda Wang <fwang@mandriva.org> 1:1.5.1-1mdv2008.0
+ Revision: 72089
- fix file list and desktop entry
- Rediff genisoimage patch
- New version 1.5.1
- use msgconv to convert po files, otherwise PO files will be invalid

* Tue Jun 12 2007 Adam Williamson <awilliamson@mandriva.org> 1:1.5-2mdv2008.0
+ Revision: 38371
- convert .po files to UTF-8 (#31297)

  + Funda Wang <fwang@mandriva.org>
    - Conditioned patch

* Thu May 24 2007 Adam Williamson <awilliamson@mandriva.org> 1:1.5-1mdv2008.0
+ Revision: 30571
- nothing in pixmaps, package fd.o icons
- screw it, drop all 2007.0 stuff in the hope we don't need to build it there again
- drop conditionals for including patch, only conditionalize application
- 1.5 final. 2007: rebuild against updated libdbus

  + Funda Wang <fwang@mandriva.org>
    - Pack pixmap dir


* Sun Mar 04 2007 Emmanuel Andry <eandry@mandriva.org> 1.5-0.beta7.1mdv2007.0
+ Revision: 131976
- update P0 to be fully genisoimage compliant (Rick James)
- fix buildrequires
- buildrequires automake1.8
- New version 1.5 beta 7
  replace mkisofs with cdrkit-genisoimage
  diff patch to support genisoimage
  xdg menu

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Import dvdstyler

* Wed Apr 12 2006 Jerome Martin <jmartin@mandriva.org> 1:1.5-0.beta5.1mdk
- beta5

* Fri Feb 03 2006 Austin Acton <austin@mandriva.org> 1:1.5-0.beta4.1mdk
- beta4

* Sun Jan 01 2006 Austin Acton <austin@mandriva.org> 1:1.5-0.beta3.1mdk
- 1.5beta3
- buildrequires wxsvg-devel
- mkrel

* Fri May 27 2005 Austin Acton <austin@mandriva.org> 1:1.4-1mdk
- 1.4
- epoch 1 to install over 1.31
- force newer wx config script

* Fri Feb 18 2005 Austin Acton <austin@mandrake.org> 1.31-1mdk
- 1.31

* Mon Jan 17 2005 Austin Acton <austin@mandrake.org> 1.3b-1mdk
- initial package

