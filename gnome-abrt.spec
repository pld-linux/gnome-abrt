#
# Conditional build:
%bcond_with	tests	# "make check" run (some pylint false positive?)

Summary:	A utility for viewing problems that have occurred with the system
Summary(pl.UTF-8):	Narzędzie do przeglądania problemów, które wystąpiły w systemie
Name:		gnome-abrt
Version:	1.2.5
Release:	6
License:	GPL v2+
Group:		Applications/System
Source0:	https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.gz
# Source0-md5:	e3ab0e2c43bb6b28f29eced47cca8d67
Patch0:		%{name}-pylint.patch
URL:		https://github.com/abrt/abrt/wiki/ABRT-Project
BuildRequires:	abrt-gui-devel >= 2.1.7
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libreport-gtk-devel >= 2.0.20
BuildRequires:	libtool
BuildRequires:	pkgconfig
%{?with_tests:BuildRequires:	pylint}
BuildRequires:	python3-devel >= 1:3.4
%{?with_tests:BuildRequires:	python3-libreport}
BuildRequires:	python3-pygobject3-devel >= 3.0
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	sed >= 4.0
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libX11-devel
Requires(post,postun):	gtk-update-icon-cache
Requires:	abrt-dbus
Requires:	abrt-gui-libs >= 2.1.7
Requires:	hicolor-icon-theme
Requires:	python3-dbus
Requires:	python3-libreport
Requires:	python3-pygobject3 >= 3.0
Requires:	python3-pyinotify
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A GNOME application allows users to browse through detected problems
and provides them with convenient way for managing these problems.

%description -l pl.UTF-8
Aplikacja GNOME pozwalająca użytkownikom przeglądać wykryte problemy i
zapewniająca wygodny sposób zarządzania tymi problemami.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's#-pedantic##g' configure.ac
%{__sed} -i -e '1s,#!/usr/bin/env python,#!/usr/bin/python,' src/gnome-abrt

%{__sed} -n -e '/^%%changelog/,$' gnome-abrt.spec.in | tail -n +2 > changelog

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_tests:--with-nopylint}

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/gnome_abrt/wrappers/*.la
%py_postclean

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/gnome-abrt/README.md

%find_lang %{name}
%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md changelog
%attr(755,root,root) %{_bindir}/gnome-abrt
%dir %{py3_sitedir}/gnome_abrt
%{py3_sitedir}/gnome_abrt/*.py
%{py3_sitedir}/gnome_abrt/__pycache__
%dir %{py3_sitedir}/gnome_abrt/url
%{py3_sitedir}/gnome_abrt/url/*.py
%{py3_sitedir}/gnome_abrt/url/__pycache__
%dir %{py3_sitedir}/gnome_abrt/wrappers
%{py3_sitedir}/gnome_abrt/wrappers/__init__.py
%{py3_sitedir}/gnome_abrt/wrappers/__pycache__
%attr(755,root,root) %{py3_sitedir}/gnome_abrt/wrappers/_wrappers.so
%{_datadir}/gnome-abrt
%{_datadir}/appdata/gnome-abrt.appdata.xml
%{_desktopdir}/gnome-abrt.desktop
%{_iconsdir}/hicolor/*x*/apps/gnome-abrt.png
%{_iconsdir}/hicolor/*x*/status/gnome-abrt.png
%{_iconsdir}/hicolor/symbolic/apps/gnome-abrt-symbolic.svg
%{_mandir}/man1/gnome-abrt.1*
