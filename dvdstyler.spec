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
