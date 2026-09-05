#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.7.4
%define		kfver		6.26.0
%define		qt_ver		6.10.0
%define		kpname		aurorae

Summary:	A themeable window decoration for KWin
Name:		kp6-%{kpname}
Version:	6.7.4
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	e3117b48474022601917b1643f629656
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6DBus-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Quick-devel >= %{qt_ver}
BuildRequires:	Qt6UiTools-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kfver}
BuildRequires:	kf6-kcmutils-devel >= %{kfver}
BuildRequires:	kf6-kcolorscheme-devel >= %{kfver}
BuildRequires:	kf6-kconfig-devel >= %{kfver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kfver}
BuildRequires:	kf6-ki18n-devel >= %{kfver}
BuildRequires:	kf6-knewstuff-devel >= %{kfver}
BuildRequires:	kf6-kpackage-devel >= %{kfver}
BuildRequires:	kf6-ksvg-devel >= %{kfver}
BuildRequires:	kp6-kdecoration-devel >= 6.7.0
BuildRequires:	libstdc++-devel >= 6:11
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Aurorae is a themeable window decoration for KWin.

%description -l pl.UTF-8
Aurorae jest systemem dekoracji okien dla KWin.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build
sed -i -e 's|/usr/bin/bash|/bin/bash|' $RPM_BUILD_ROOT%{_prefix}/libexec/plasma-apply-aurorae

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%doc AUTHORS README TODO theme-description
%{_libdir}/cmake/Aurorae
%{_libdir}/qt6/plugins/org.kde.kdecoration3.kcm/kcm_auroraedecoration.so
%{_libdir}/qt6/plugins/org.kde.kdecoration3/org.kde.kwin.aurorae.so
%{_libdir}/qt6/plugins/org.kde.kdecoration3/org.kde.kwin.aurorae.v2.so
%dir %{_libdir}/qt6/qml/org/kde/kwin/decoration
%{_libdir}/qt6/qml/org/kde/kwin/decoration/AppMenuButton.qml
%{_libdir}/qt6/qml/org/kde/kwin/decoration/ButtonGroup.qml
%{_libdir}/qt6/qml/org/kde/kwin/decoration/Decoration.qml
%{_libdir}/qt6/qml/org/kde/kwin/decoration/DecorationButton.qml
%{_libdir}/qt6/qml/org/kde/kwin/decoration/MenuButton.qml
%{_libdir}/qt6/qml/org/kde/kwin/decoration/decorationplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/kwin/decoration/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/kwin/decoration/libdecorationplugin.so
%{_libdir}/qt6/qml/org/kde/kwin/decoration/qmldir
%{_libdir}/qt6/qml/org/kde/kwin/decorations/plastik/libplastikplugin.so
%dir %{_libdir}/qt6/qml/org/kde/kwin/decorations
%dir %{_libdir}/qt6/qml/org/kde/kwin/decorations/plastik
%{_libdir}/qt6/qml/org/kde/kwin/decorations/plastik/qmldir
%attr(755,root,root) %{_prefix}/libexec/plasma-apply-aurorae
%{_datadir}/knsrcfiles/aurorae.knsrc
%{_datadir}/kwin/aurorae
%{_datadir}/kwin/decorations
