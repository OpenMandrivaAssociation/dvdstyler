%define oname DVDStyler

Name:		dvdstyler
Summary:	DVD authoring application
Version:	2.9.2
Release:	1
Epoch:		1
Source0:	http://sourceforge.net/projects/dvdstyler/files/%{name}/%{version}/%{oname}-%{version}.tar.bz2
URL:		http://dvdstyler.sourceforge.net/
License:	GPLv2+
Group:		Video
BuildRequires:	bison
BuildRequires:	desktop-file-utils
BuildRequires:	dvd+rw-tools
BuildRequires:	dvdauthor >= 0.7.0
BuildRequires:	ffmpeg
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	imagemagick
BuildRequires:	mkisofs
BuildRequires:	netpbm
BuildRequires:	xmlto
BuildRequires:	zip
BuildRequires:	ffmpeg-devel
BuildRequires:	wxgtku2.8-devel
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libwxsvg) >= 1.1.14
BuildRequires:	pkgconfig(udev)

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
%setup -q -n %{oname}-%{version}
# fix desktop file
sed -i -e 's,%{name}.png,%{name},g' data/dvdstyler.desktop

# not utf-8 file
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog

%build
chmod +x ./autogen.sh ./configure
./autogen.sh
%configure --with-wx-config=%{_bindir}/wx-config-unicode
%make

%install
%makeinstall_std
# we'll install this in %%files section
rm -fr %{buildroot}%{_docdir}

# menu entry
desktop-file-install --vendor='' \
	--dir=%{buildroot}%{_datadir}/applications \
	--remove-category='Application' \
	--add-category='Video;AudioVideoEditing' \
	%{buildroot}%{_datadir}/applications/*.desktop

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -size 48x48 src/rc/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -size 32x32 src/rc/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -size 16x16 src/rc/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# remove duplicate files
rm -fr %{buildroot}%{_libdir}/share/doc/dvdstyler/

# es_ar language missing in rosa lang tree, to be seen later
# for now we got to live with "E: invalid-lc-messages-dir"
# I'd like to avoid rpmlintrc usage.
# If someone have a fix please push it.

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
%{_iconsdir}/hicolor/*/apps/%{name}.png
