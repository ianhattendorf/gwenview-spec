
# Fedora Core 2 support.
%define fedora_release %(if test -n "$(rpm -ql fedora-release | grep -m1 etc)";  then rpm -q --qf "%%{version}" fedora-release; else echo 0; fi )
%if "%fedora_release" > "1"
%define target_kde32 1
%endif
%{?_with_kde32: %define target_kde32 1}

Name:           gwenview
Version:        1.0.1
Release:        0.fdr.4.1.90
Epoch:          0
Summary:        Simple image viewer for KDE.

Group:          Applications/Multimedia
License:        GPL
URL:            http://gwenview.sf.net
Source0:        http://dl.sf.net/gwenview/gwenview-1.0.1.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs-devel >= 6:3.0.0, arts-devel
BuildRequires:  XFree86-devel, zlib-devel, libjpeg-devel
BuildRequires:  libart_lgpl-devel, desktop-file-utils
BuildRequires:  libpng-devel, gettext

%if 0%{?target_kde32}
BuildRequires:  libmng-devel fam-devel glib2-devel
%endif


%description
Gwenview is an image viewer for KDE. 

It features a folder tree window and a file list window to provide easy 
navigation in your file hierarchy.  Image loading is done by the Qt library, 
so it supports all image formats your Qt installation supports. 


%prep
%setup -q
perl -pi -e 's,Categories=Qt;KDE;Graphics,Categories=Qt;KDE;Graphics;,' desktopfiles/gwenview.desktop
perl -pi -e 's,Commend\[ko\]=,Comment\[ko\]=,' desktopfiles/gwenview.desktop

%build
[ -n "$QTDIR" ] || . %{_sysconfdir}/profile.d/qt.sh
%configure --disable-rpath \
           --disable-debug \
           --enable-final
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor fedora --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Fedora \
  --add-category Application \
  --add-category Viewer \
  $RPM_BUILD_ROOT%{_datadir}/applications/kde/%{name}.desktop

# KDE 3.2:
%if 0%{?target_kde32}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/kde
mv $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop $RPM_BUILD_ROOT%{_datadir}/applications/kde/
%endif


rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{xx,ven,nso}

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO CREDITS
%{_bindir}/*
%if 0%{?target_kde32}
%{_datadir}/applications/kde/*.desktop
%else
%{_datadir}/applications/*.desktop
%endif
%{_datadir}/apps/konqueror/servicemenus/*
%{_datadir}/icons/*/*/apps/*
%{_datadir}/apps/%{name}
%{_mandir}/man1/*


%changelog
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
