%define name	dvdstyler
%define version	1.5.1
%define relindex 2
%define release %mkrel 1

Name: 	 	%{name}
Summary: 	DVD authoring GUI
Version: 	%{version}
Release: 	%{release}
Epoch:		1
Source:		http://prdownloads.sourceforge.net/dvdstyler/DVDStyler-%{version}_%{relindex}.tar.gz
Patch0:		dvdstyler-genisoimage.patch
URL:		http://dvdstyler.sourceforge.net/
License:	GPL
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	pkgconfig ImageMagick
BuildRequires:	wxsvg-devel >= 1.0-0.beta6
BuildRequires:	kdelibs-common libgnomeui2-devel automake1.8
BuildRequires:	dvdauthor mjpegtools netpbm mpgtx dvd+rw-tools
Requires:	dvdauthor mjpegtools netpbm mpgtx dvd+rw-tools
BuildRequires:	mkisofs
Requires:	mkisofs
BuildRequires:	gettext

%description
The main DVDStyler features are:
    * you can drag and drop MPEG files directly
    * you can import image file for background
    * you can create NTSC/PAL menu
    * you can place text and images anywhere on the menu screen
    * you can change font/color
    * you can put basic text buttons, change font/color and background color
    * you can set chapters for each movie
    * you can change post command for each movie

%prep
%setup -q -n DVDStyler-%{version}_%{relindex}
%if %mdkversion > 200700
%patch0
#needed by patch0
./autogen.sh
%endif

%build
# Convert .po files to UTF-8: bug #31297 - AdamW 2007/06
pushd locale
for i in *.po; do msgconv -t UTF-8 $i -o $i.new; mv -f $i.new $i; done
popd
%configure2_5x --prefix=%_libdir --with-wx-config=%_bindir/wx-config-ansi
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -fr %buildroot/%{_docdir}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=DVDStyler
Comment=%{Summary}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Video;AudioVideo;Video;AudioVideoEditing;
Encoding=UTF-8
EOF

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 src/rc/%name.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 src/rc/%name.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 src/rc/%name.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

#fd.o icons

mkdir -p $RPM_BUILD_ROOT/%_iconsdir/hicolor/{48x48,32x32,16x16}/apps
convert -size 48x48 src/rc/%name.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/48x48/apps/%name.png
convert -size 32x32 src/rc/%name.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/32x32/apps/%name.png
convert -size 16x16 src/rc/%name.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/16x16/apps/%name.png

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%update_icon_cache hicolor
		
%postun
%clean_menus
%clean_icon_cache hicolor

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%name
%{_datadir}/%name
%{_datadir}/applications/mandriva-%{name}.desktop
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
%{_iconsdir}/hicolor/48x48/apps/%name.png
%{_iconsdir}/hicolor/32x32/apps/%name.png
%{_iconsdir}/hicolor/16x16/apps/%name.png
