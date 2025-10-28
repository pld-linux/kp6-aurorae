#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.5.1
%define		qt_ver		6.8.0
%define		kpname		aurorae

Summary:	A themeable window decoration for KWin
Name:		kp6-%{kpname}
Version:	6.5.1
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	f10fb8a69d0fb30b95a17da289ab191d
URL:		http://www.kde.org/
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= 6.14.0
BuildRequires:	kf6-kcmutils-devel >= 6.14.0
BuildRequires:	kf6-kcolorscheme-devel >= 6.15.0
BuildRequires:	kf6-kconfig-devel >= 6.14.0
BuildRequires:	kf6-kcoreaddons-devel >= 6.15.0
BuildRequires:	kf6-ki18n-devel >= 6.14.0
BuildRequires:	kf6-knewstuff-devel >= 6.14.0
BuildRequires:	kf6-kpackage-devel >= 6.14.0
BuildRequires:	kp6-kdecoration-devel >= %{kdeplasmaver}
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Aurorae is a themeable window decoration for KWin.

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
%dir %{_libdir}/qt6/qml/org/kde/kwin/decoration
%{_libdir}/qt6/qml/org/kde/kwin/decoration/AppMenuButton.qml
%{_libdir}/qt6/qml/org/kde/kwin/decoration/ButtonGroup.qml
%{_libdir}/qt6/qml/org/kde/kwin/decoration/Decoration.qml
%{_libdir}/qt6/qml/org/kde/kwin/decoration/DecorationButton.qml
%{_libdir}/qt6/qml/org/kde/kwin/decoration/MenuButton.qml
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
