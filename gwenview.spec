Name:    gwenview 
Summary: An image viewer
Version: 15.08.0
Release: 1%{?dist}

# app: GPLv2+
# lib:  IJG and (LGPLv2 or LGPLv3 or LGPLv3+ (KDE e.V.)) and LGPLv2+ and GPLv2+
License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdegraphics/gwenview
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif 
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

## upstreamable patches

BuildRequires: cmake 
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-kactivities-devel
buildRequires: kf5-kdelibs4support-devel
BuildRequires: kf5-kio-devel
## frameworks soon to come (hopefully) -- rex
#BuildRequires: kf5-kdcraw-devel
#BuildRequires: kf5-kipi-devel
BuildRequires: libappstream-glib
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig(exiv2)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(phonon4qt5)
BuildRequires: pkgconfig(Qt5DBus) pkgconfig(Qt5Widgets) pkgconfig(Qt5Script) pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5Concurrent) pkgconfig(Qt5Svg) pkgconfig(Qt5OpenGL)
BuildRequires: pkgconfig(Qt5X11Extras)

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

# when split occurred
Conflicts: kdegraphics < 7:4.6.95-10

%description
%{summary}.

%package  libs 
Summary:  Runtime files for %{name} 
# wrt (LGPLv2 or LGPLv3), KDE e.V. may determine that future GPL versions are accepted 
License:  IJG and LGPLv2+ and GPLv2+ and LGPLv2 or LGPLv3
Requires: %{name} = %{version}-%{release}
%description libs 
%{summary}.


%prep
%setup -q


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
appstream-util validate-relax --nonet %{buildroot}%{_kf5_datadir}/appdata/%{name}.appdata.xml ||:
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/org.kde.%{name}.desktop


%post
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%files 
%doc COPYING 
%{_kf5_bindir}/%{name}*
%{_kf5_datadir}/applications/org.kde.%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_kf5_datadir}/icons/hicolor/*/*/*
%{_kf5_docdir}/HTML/en/gwenview/
%{_kf5_datadir}/gvpart/
%{_kf5_datadir}/kservices5/gvpart.desktop
%{_kf5_datadir}/gwenview/
%{_kf5_datadir}/kservices5/ServiceMenus/slideshow.desktop
%{_kf5_datadir}/kxmlgui5/gwenview/

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kf5_libdir}/libgwenviewlib.so.*
%{_kf5_qtplugindir}/gvpart.so


%changelog
* Thu Aug 20 2015 Than Ngo <than@redhat.com> - 15.08.0-1
- 15.08.0

* Wed Jun 24 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.04.2-3
- rebuild (exiv2)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.04.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.04.2-1
- 15.04.2

* Wed May 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.04.1-1
- 15.04.1

* Wed Apr 15 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.04.0-1
- 15.04.0

* Sat Jan 17 2015 Rex Dieter <rdieter@fedoraproject.org> 4.14.3-4
- kde-applications fixes, cleanup

* Wed Nov 26 2014 Rex Dieter <rdieter@fedoraproject.org> 4.14.3-3
- drop libjpeg-turbo workaround

* Mon Nov 17 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.3-2
- fix/workaround FTBFS against new libjpeg-turbo (#1163476)
- use %%find_lang

* Sat Nov 08 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.3-1
- 4.14.3

* Fri Nov 07 2014 Rex Dieter <rdieter@fedoraproject.org> 4.14.2-2
- pull in appdata from upstream master/ branch 

* Sun Oct 12 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.2-1
- 4.14.2

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.1-1
- 4.14.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.0-1
- 4.14.0

* Tue Aug 05 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.97-1
- 4.13.97

* Tue Jul 15 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.3-1
- 4.13.3

* Mon Jun 09 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.2-1
- 4.13.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 11 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.1-1
- 4.13.1

* Sat Apr 12 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.0-1
- 4.13.0

* Fri Apr 04 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.97-1
- 4.12.97

* Sat Mar 22 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.95-1
- 4.12.95

* Wed Mar 19 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.90-1
- 4.12.90

* Sun Mar 02 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.3-1
- 4.12.3

* Fri Jan 31 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.2-1
- 4.12.2

* Fri Jan 10 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.1-1
- 4.12.1

* Thu Dec 19 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.12.0-1
- 4.12.0

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.97-2
- rebuild (exiv2)

* Sun Dec 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.97-1
- 4.11.97

* Thu Nov 21 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.95-1
- 4.11.95

* Sat Nov 16 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.90-1
- 4.11.90

* Sat Nov 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.3-1
- 4.11.3

* Sat Sep 28 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.2-1
- 4.11.2

* Wed Sep 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.1-1
- 4.11.1

* Thu Aug 08 2013 Than Ngo <than@redhat.com> - 4.11.0-1
- 4.11.0

* Thu Jul 25 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.97-1
- 4.10.97

* Tue Jul 23 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.95-1
- 4.10.95

* Fri Jun 28 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.90-1
- 4.10.90

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Sun Mar 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Fri Feb 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Tue Jan 22 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 4.9.97-2
- rebuild due to "jpeg8-ABI" feature drop

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.90-1
- 4.9.90

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Wed Oct 24 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.2-2
- rebuild (libjpeg-turbo v8)

* Sat Sep 29 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Fri Sep 21 2012 Alexey Kurov <nucleo@fedoraproject.org> - 4.9.1-2
- rebuild (libkipi)

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Mon Aug 6 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-2
- stop the thumbnailing when Gwenview exits; This is important as it
  blocks unmounting of flash drives

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.95-1
- 4.8.95

* Sat Jun 09 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.90-1
- 4.8.90

* Fri Jun 01 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-1
- 4.8.80

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.3-2
- rebuild (exiv2)

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- 4.8.2

* Mon Mar 12 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.1-2
- gvpart fixes (#784683,kde#292394)

* Mon Mar 05 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.1-1
- 4.8.1

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.7.97-1
- 4.7.97

* Wed Dec 21 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.7.90-1
- 4.7.90

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-1
- 4.7.80

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.7.2-2
- rebuild (exiv2)

* Wed Oct 05 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Wed Sep 14 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.1-2
- Make BR: kdebase4-devel versioned

* Fri Sep 02 2011 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.0-1
- 4.7.0

* Mon Jul 18 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-2
- License: GPLv2+
- -libs: License: IJG and LGPLv2+ and GPLv2+ and LGPLv2 or LGPLv3
- %%postun: +update-desktop-database

* Mon Jul 11 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-1
- 4.6.95
- update URL 

* Wed Jul 06 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-2
- fix Source0 URL
- Conflicts: kdegraphics < 7:4.6.90-10

* Tue Jul 05 2011 Rex Dieter <rdieter@fedoraproject.org>  4.6.90-1
- first try

