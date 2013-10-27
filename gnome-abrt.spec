#
# Conditional build:
%bcond_with	tests	# "make check" run (some pylint false positive?)

Summary:	A utility for viewing problems that have occurred with the system
Summary(pl.UTF-8):	Narzędzie do przeglądania problemów, które wystąpiły w systemie
Name:		gnome-abrt
Version:	0.3.3
Release:	2
License:	GPL v2+
Group:		Applications/System
Source0:	https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.gz
# Source0-md5:	ba51ea0a7684d164f57740ff3ab81d26
Patch0:		%{name}-pylint.patch
URL:		https://fedorahosted.org/abrt/
BuildRequires:	abrt-gui-devel >= 2.1.7
BuildRequires:	asciidoc
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libreport-gtk-devel >= 2.0.20
%{?with_tests:BuildRequires:	libreport-python}
BuildRequires:	pkgconfig
%{?with_tests:BuildRequires:	pylint}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-pygobject3-devel >= 3.0
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	sed >= 4.0
BuildRequires:	xmlto
Requires(post,postun):	gtk-update-icon-cache
Requires:	abrt-gui-libs >= 2.1.7
Requires:	hicolor-icon-theme
Requires:	libreport-python
Requires:	python-dbus
Requires:	python-pyinotify
Requires:	python-pygobject3
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

%{__sed} -i -e '1s,#!/usr/bin/env python,#!/usr/bin/python,' src/gnome-abrt

%build
%configure \
	--disable-silent-rules \
	%{!?with_tests:--with-nopylint}

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/gnome_abrt/wrappers/*.la
%py_postclean

# just a copy of cs
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/cs_CZ

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gnome-abrt
%dir %{py_sitedir}/gnome_abrt
%{py_sitedir}/gnome_abrt/*.py[co]
%dir %{py_sitedir}/gnome_abrt/url
%{py_sitedir}/gnome_abrt/url/*.py[co]
%dir %{py_sitedir}/gnome_abrt/wrappers
%{py_sitedir}/gnome_abrt/wrappers/__init__.py[co]
%attr(755,root,root) %{py_sitedir}/gnome_abrt/wrappers/_wrappers.so
%{_datadir}/gnome-abrt
%{_datadir}/appdata/gnome-abrt.appdata.xml
%{_desktopdir}/gnome-abrt.desktop
%{_iconsdir}/hicolor/*/apps/gnome-abrt.png
%{_iconsdir}/hicolor/*/status/gnome-abrt.png
%{_mandir}/man1/gnome-abrt.1*
