#
# Conditional build:
%bcond_with	tests	# "make check" run (some pylint false positive?)

Summary:	A utility for viewing problems that have occurred with the system
Summary(pl.UTF-8):	Narzędzie do przeglądania problemów, które wystąpiły w systemie
Name:		gnome-abrt
Version:	1.5.2
Release:	1
License:	GPL v2+
Group:		Applications/System
#Source0Download: https://github.com/abrt/gnome-abrt/releases
Source0:	https://github.com/abrt/gnome-abrt/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	19a5b30aaa20b0e8013d749de4d77dde
URL:		https://github.com/abrt/abrt/wiki/gnome-abrt
BuildRequires:	abrt-gui-devel >= 2.14.0
BuildRequires:	asciidoc
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	gtk4-devel >= 4.0
BuildRequires:	libadwaita-devel
BuildRequires:	libreport-gtk-devel >= 2.14.0
BuildRequires:	meson >= 0.63.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
%{?with_tests:BuildRequires:	py3lint}
BuildRequires:	python3-devel >= 1:3.4
%{?with_tests:BuildRequires:	python3-humanize}
%{?with_tests:BuildRequires:	python3-libreport}
BuildRequires:	python3-pygobject3-devel >= 3.29.1
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRequires:	xmlto
Requires(post,postun):	gtk-update-icon-cache
Requires:	abrt-dbus >= 2.14.0
Requires:	abrt-gui-libs >= 2.14.0
# Gtk-4.0.typelib
Requires:	gtk4 >= 4.0
Requires:	hicolor-icon-theme
# Adw-1.typelib
Requires:	libadwaita
Requires:	libreport-gtk >= 2.14.0
Requires:	python3-bs4
Requires:	python3-dbus
Requires:	python3-humanize
Requires:	python3-libreport >= 2.14.0
Requires:	python3-pygobject3 >= 3.29.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A GNOME application allows users to browse through detected problems
and provides them with convenient way for managing these problems.

%description -l pl.UTF-8
Aplikacja GNOME pozwalająca użytkownikom przeglądać wykryte problemy i
zapewniająca wygodny sposób zarządzania tymi problemami.

%prep
%setup -q

%build
%meson \
	%{?with_tests:-Dlint=true}

%meson_build

%if %{with tests}
%meson_test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/gnome-abrt
%dir %{py3_sitedir}/gnome_abrt
%{py3_sitedir}/gnome_abrt/*.py
%{py3_sitedir}/gnome_abrt/__pycache__
%dir %{py3_sitedir}/gnome_abrt/wrappers
%{py3_sitedir}/gnome_abrt/wrappers/__init__.py
%{py3_sitedir}/gnome_abrt/wrappers/__pycache__
%attr(755,root,root) %{py3_sitedir}/gnome_abrt/wrappers/_wrappers.cpython-*.so
%{_datadir}/gnome-abrt
%{_datadir}/metainfo/org.freedesktop.GnomeAbrt.appdata.xml
%{_desktopdir}/org.freedesktop.GnomeAbrt.desktop
%{_iconsdir}/hicolor/scalable/apps/org.freedesktop.GnomeAbrt.svg
%{_iconsdir}/hicolor/symbolic/apps/org.freedesktop.GnomeAbrt-symbolic.svg
%{_mandir}/man1/gnome-abrt.1*
