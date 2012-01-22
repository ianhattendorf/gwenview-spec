Name:    gwenview 
Summary: An image viewer
Version: 4.8.0
Release: 1%{?dist}

# app: GPLv2+
# lib:  IJG and (LGPLv2 or LGPLv3 or LGPLv3+ (KDE e.V.)) and LGPLv2+ and GPLv2+
License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdegraphics/gwenview 
Source0: ftp://ftp.kde.org/pub/kde/unstable/%{version}/src/%{name}-%{version}.tar.bz2

BuildRequires: desktop-file-utils
# libkonq
BuildRequires: kdebase4-devel >= %{version}
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: libkipi-devel >= %{version}
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig(exiv2)

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdebase-runtime%{?_kde4_version: >= %{_kde4_version}}

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
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# unpackaged files
rm -fv %{buildroot}%{_kde4_libdir}/libgwenviewlib.so


%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/gwenview.desktop


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null ||:
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%doc COPYING 
%{_kde4_bindir}/%{name}*
%{_kde4_appsdir}/%{name}/
%{_kde4_appsdir}/solid/actions/%{name}*.desktop
%{_kde4_datadir}/kde4/services/ServiceMenus/*.desktop
%{_kde4_datadir}/applications/kde4/%{name}.desktop
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_docdir}/HTML/en/%{name}/
# split gvpart?
%{_kde4_appsdir}/gvpart/
%{_kde4_datadir}/kde4/services/gvpart.desktop
%{_kde4_libdir}/kde4/gvpart.so

%files libs
%doc lib/libjpeg-80/README.jpeg
%{_kde4_libdir}/libgwenviewlib.so.4*


%changelog
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

