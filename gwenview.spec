Name:           gwenview
Version:        1.4.1
Release:        3%{?dist}
Summary:        Simple image viewer for KDE

Group:          Applications/Multimedia
License:        GPL
URL:            http://gwenview.sf.net
Source0:        http://dl.sf.net/gwenview/gwenview-%{version}.tar.bz2
Source1:        http://dl.sf.net/gwenview/gwenview-i18n-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs-devel >= 6:3.1
BuildRequires:  desktop-file-utils
BuildRequires:  libkipi-devel
BuildRequires:  gettext
BuildRequires:  exiv2-devel
%if "%{fedora}" >= "5"
BuildRequires:  libXt-devel
%endif

# Maybe I'll split it in the future
Provides:       gwenview-i18n = %{version}-%{release}


%description
Gwenview is an image viewer for KDE.

It features a folder tree window and a file list window to provide easy
navigation in your file hierarchy.  Image loading is done by the Qt library,
so it supports all image formats your Qt installation supports.


%prep
%setup -q -a 1


%build
unset QTDIR && . %{_sysconfdir}/profile.d/qt.sh
# work around an improper ${kdelibsuff}
export QTLIB=${QTDIR}/lib QTINC=${QTDIR}/include
%configure --disable-rpath --disable-debug --enable-kipi
# --enable-final  \
make %{?_smp_mflags}

cd %{name}-i18n-%{version}
%configure
make %{?_smp_mflags}
cd ..


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor fedora --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/kde \
  --add-category X-Fedora \
  --add-category Application \
  --add-category Viewer \
  $RPM_BUILD_ROOT%{_datadir}/applications/kde/%{name}.desktop

cd %{name}-i18n-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

# Files list
%find_lang %{name}

# HTML help
for lang_dir in $RPM_BUILD_ROOT%{_datadir}/doc/HTML/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) %{_datadir}/doc/HTML/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && rm -f $i/common && ln -sf ../common $i/common
      done
    popd
  fi
done


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README TODO
%{_bindir}/*
%{_datadir}/applications/kde/*.desktop
%{_datadir}/apps/konqueror/servicemenus/*
%{_datadir}/icons/*/*/apps/*
%{_datadir}/apps/gwenview
%{_datadir}/apps/gvdirpart
%{_datadir}/apps/gvimagepart
%{_datadir}/apps/kconf_update
%{_datadir}/services/*.desktop
%{_datadir}/config.kcfg/*.kcfg
%{_mandir}/man1/*
%{_libdir}/lib*
%{_libdir}/kde3/lib*
%{_libdir}/kde3/gwenview.*


%changelog
* Wed Nov 29 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4.1-3
- rebuild

* Mon Nov 27 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4.1-2
- remove patch (gwenview now uses exiv2 instead of libexif)

* Mon Nov 27 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4.1-1
- version 1.4.1

* Tue Oct 03 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4.0-3
- patch for latest libexif-devel

* Tue Oct 03 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4.0-2
- missing BR: libexif-devel

* Tue Oct 03 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.4.0-1
- version 1.4.0

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.3.1-6
- rebuild

* Tue Apr 11 2006 Aurelien Bompard <gauret[AT]free.fr> 1.3.1-5
- fix build outside the buildsystem (bug 188486)

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 1.3.1-4
- rebuild for fc5

* Thu Nov 24 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.1-3
- fix build with modular Xorg

* Wed Nov 23 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.1-2
- fix build (qt env var)

* Sun Nov 20 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.1-1
- version 1.3.1
- drop patch0

* Mon Sep 12 2005 Aurelien Bompard <gauret[AT]free.fr> 1.3.0-1
- version 1.3.0

* Thu Jun  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-4.fc4
- temporarily add patch to work around Fedora Core bug 159090

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 1.2.0-3.fc4
- fix build on 64bit systems (#158887)

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.2.0-2.fc4
- rebuild on all arches

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
