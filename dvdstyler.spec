%define oname	DVDStyler
%define srcname 1.7.4_3

Name: 	 	dvdstyler
Summary: 	DVD authoring application
Version: 	1.7.4
Release: 	%mkrel 2
Epoch:		1
Source0:	http://downloads.sourceforge.net/%{name}/%{oname}-%{srcname}.tar.bz2
Patch0:		dvdstyler-genisoimage.patch
URL:		http://dvdstyler.sourceforge.net/
License:	GPL+
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	imagemagick
BuildRequires:	wxsvg-devel >= 1.0-1mdv
BuildRequires:	libgnomeui2-devel
BuildRequires:	dvdauthor
BuildRequires:	netpbm
BuildRequires:	dvd+rw-tools
BuildRequires:	mkisofs
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
Buildrequires:	libexif-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	xmlto
BuildRequires:	zip
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
%setup -q -n %{oname}-%{srcname}
%patch0 -p1
#needed by patch0
./autogen.sh

%build
# Convert .po files to UTF-8: bug #31297 - AdamW 2007/06
pushd locale
for i in *.po; do msgconv -t UTF-8 $i -o $i.new; mv -f $i.new $i; done
popd
%define Werror_cflags %nil
%configure2_5x --prefix=%{_libdir} --with-wx-config=%{_bindir}/wx-config-ansi
%make
										
%install
rm -rf %{buildroot}
%makeinstall_std
rm -fr %{buildroot}/%{_docdir}

desktop-file-install --vendor='' \
	--dir=%{buildroot}%{_datadir}/applications \
	--remove-category='Application' \
	--add-category='Video;AudioVideoEditing' \
	%{buildroot}%{_datadir}/applications/*.desktop

mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -size 48x48 src/rc/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -size 32x32 src/rc/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -size 16x16 src/rc/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png

#remove duplicate files
rm -fr %{buildroot}/%{_libdir}/share/doc/dvdstyler/


%find_lang %{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif
		
%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
