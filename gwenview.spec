Name:           gwenview
Version:        1.2.0
Release:        1.fc4

Summary:        Simple image viewer for KDE

Group:          Applications/Multimedia
License:        GPL
URL:            http://gwenview.sf.net
Source0:        http://dl.sf.net/gwenview/gwenview-1.2.0.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs-devel >= 6:3.1
BuildRequires:  desktop-file-utils
BuildRequires:  libkipi-devel
BuildRequires:  gettext
#BuildRequires:  fam-devel glib2-devel

%description
Gwenview is an image viewer for KDE.

It features a folder tree window and a file list window to provide easy
navigation in your file hierarchy.  Image loading is done by the Qt library,
so it supports all image formats your Qt installation supports.


%prep
%setup -q

%build
[ -n "$QTDIR" ] || . %{_sysconfdir}/profile.d/qt.sh
%configure --disable-rpath \
           --disable-debug \
           --enable-kipi
# --enable-final  \
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor fedora --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/kde \
  --add-category X-Fedora \
  --add-category Application \
  --add-category Viewer \
  $RPM_BUILD_ROOT%{_datadir}/applications/kde/%{name}.desktop

%find_lang %{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO CREDITS
%{_bindir}/*
%{_datadir}/applications/kde/*.desktop
%{_datadir}/apps/konqueror/servicemenus/*
%{_datadir}/icons/*/*/apps/*
%{_datadir}/apps/*
%{_datadir}/services/*.desktop
%{_mandir}/man1/*
%{_libdir}/lib*
%{_libdir}/kde3/lib*
%{_libdir}/kde3/gwenview.*
%{_datadir}/doc/HTML/en/gwenview


%changelog
* Fri Apr 08 2005 Aurelien Bompard <gauret[AT]free.fr> 1.2.0-1.fc4
- version 1.2.0
- change release tag for FC4

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Nov 24 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1.6-2
- remove hardcoded requirement to kipi-plugins

* Mon Oct 25 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.1.6-0.fdr.1
- version 1.1.6
- drop FC1 support

* Wed Mar 17 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.1-0.fdr.4
- fix typo in desktop file

* Tue Mar 16 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.1-0.fdr.3
- apply fedora.us suggestions (#1386) :
  - fix desktop file
  - prepare for FC2
  - remove explicit requires, rpm handles this

* Mon Mar 15 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.1-0.fdr.2
- requires libjpeg to rotate and flip images
- remove desktop file category AudioVideo

* Sun Mar 14 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.1-0.fdr.1
- Initial RPM release.
