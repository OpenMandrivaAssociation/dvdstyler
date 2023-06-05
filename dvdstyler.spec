%define _disable_lto 1

Summary:	DVD authoring application
Name:		dvdstyler
Version:	3.2.1
Release:	1
Epoch:		1
License:	GPLv2+
Group:		Video
Url:		https://www.dvdstyler.org
Source0:	https://sourceforge.net/projects/dvdstyler/files/%{name}/%{version}/DVDStyler-%{version}.tar.bz2
# (upstream)
Patch0:		dvdstyler-3.2.1-fix-build-with-wxwidgets31.patch
# (gentoo)
Patch1:		ffmpeg5.patch
BuildRequires:	bison
BuildRequires:	dvd+rw-tools
BuildRequires:	dvdauthor
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	imagemagick
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libwxsvg)
BuildRequires:	pkgconfig(udev)
BuildRequires:	mkisofs
BuildRequires:	netpbm
BuildRequires:	xmlto
BuildRequires:	wxgtku3.2-devel
BuildRequires:	zip

Requires:	dvd+rw-tools
Requires:	dvdauthor
Requires:	mjpegtools
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
    * you can change post command for each movie.

%files -f %{name}.lang
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.png

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n DVDStyler-%{version}

%build
export CXXFLAGS="%{optflags} -Wno-register"
%configure	--with-wx-config="%{_bindir}/wx-config"
%make_build


%install
%make_install

# we'll install this in %%files section
rm -fr %{buildroot}%{_docdir}

# .desktop
desktop-file-install --vendor='' \
	--dir=%{buildroot}%{_datadir}/applications \
	--remove-key='Version' \
	--remove-category='Application' \
	--add-category='Video;AudioVideoEditing' \
	%{buildroot}%{_datadir}/applications/%{name}.desktop

# icnos
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -size "${d}x${d}" src/rc/%{name}.png \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done

# remove duplicate files
rm -fr %{buildroot}%{_libdir}/share/doc/dvdstyler/

# locales
%find_lang %{name}

