%define name	dvdstyler
%define version	1.5
%define release %mkrel 0.beta7.1
%define src_release b7_1

Name: 	 	%{name}
Summary: 	DVD authoring GUI
Version: 	%{version}
Release: 	%{release}
Epoch:		1

Source:		http://prdownloads.sourceforge.net/dvdstyler/DVDStyler-%{version}%{src_release}.tar.bz2
Patch0:		dvdstyler-genisoimage.patch
URL:		http://dvdstyler.sourceforge.net/
License:	GPL
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	pkgconfig ImageMagick
BuildRequires:	wxsvg-devel >= 1.0-0.beta6
BuildRequires:	kdelibs-common libgnomeui2-devel automake1.8
BuildRequires:	dvdauthor mjpegtools netpbm mpgtx cdrkit-genisoimage dvd+rw-tools
Requires:	dvdauthor mjpegtools netpbm mpgtx cdrkit-genisoimage dvd+rw-tools

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
%setup -q -n DVDStyler-%{version}%{src_release}
%patch0

#needed by patch0
./autogen.sh

%build
%configure2_5x --prefix=%_libdir --with-wx-config=%_bindir/wx-config-ansi
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -fr %buildroot/%{_docdir}

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="%{name}" icon="%{name}.png" needs="x11" title="DVDStyler" longtitle="DVD authoring GUI" section="Multimedia/Video" xdg="true"
EOF

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

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
		
%postun
%clean_menus

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%name
%{_datadir}/%name
%{_datadir}/applications/mandriva-%{name}.desktop
%{_menudir}/%name
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png



