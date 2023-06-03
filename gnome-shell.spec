## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global tarball_version %%(echo %{version} | tr '~' '.')

%global toolchain gcc

Name:           gnome-shell
Version:        44.2
Release:        personal_%autorelease
Summary:        Window management and application launching for GNOME

License:        GPLv2+
URL:            https://wiki.gnome.org/Projects/GnomeShell
Source0:        https://download.gnome.org/sources/gnome-shell/44/%{name}-%{tarball_version}.tar.xz

# Replace Epiphany with Firefox in the default favourite apps list
Patch10001: gnome-shell-favourite-apps-firefox.patch

# Some users might have a broken PAM config, so we really need this
# downstream patch to stop trying on configuration errors.
Patch40001: 0001-gdm-Work-around-failing-fingerprint-auth.patch

%define eds_version 3.45.1
%define gnome_desktop_version 40
%define glib2_version 2.56.0
%define gobject_introspection_version 1.49.1
%define gjs_version 1.73.1
%define gtk3_version 3.15.0
%define gtk4_version 4.0.0
%define adwaita_version 1.0.0
%define mutter_version 44.0
%define polkit_version 0.100
%define gsettings_desktop_schemas_version 42~beta
%define ibus_version 1.5.2
%define gnome_bluetooth_version 1:42.3
%define gstreamer_version 1.4.5
%define pipewire_version 0.3.0
%define gnome_settings_daemon_version 3.37.1

BuildRequires:  bash-completion
BuildRequires:  clang
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  git
BuildRequires:  pkgconfig(ibus-1.0) >= %{ibus_version}
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(libedataserver-1.2) >= %{eds_version}
BuildRequires:  pkgconfig(gcr-4)
BuildRequires:  pkgconfig(gjs-1.0) >= %{gjs_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnome-autoar-0)
BuildRequires:  pkgconfig(gnome-desktop-4)
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= %{gobject_introspection_version}
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(polkit-agent-1) >= %{polkit_version}
BuildRequires:  pkgconfig(libstartup-notification-1.0)
BuildRequires:  pkgconfig(libsystemd)
# for screencast recorder functionality
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= %{gstreamer_version}
BuildRequires:  pkgconfig(libpipewire-0.3) >= %{pipewire_version}
BuildRequires:  pkgconfig(gdk-x11-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  gettext >= 0.19.6
BuildRequires:  python3

# for barriers
BuildRequires:  libXfixes-devel >= 5.0
# used in unused BigThemeImage
BuildRequires:  librsvg2-devel
BuildRequires:  mutter-devel >= %{mutter_version}
BuildRequires:  pkgconfig(libpulse)
%ifnarch s390 s390x ppc ppc64 ppc64p7
BuildRequires:  gnome-bluetooth-libs-devel >= %{gnome_bluetooth_version}
%endif
# Bootstrap requirements
BuildRequires: gtk-doc
%ifnarch s390 s390x
Recommends:     gnome-bluetooth%{?_isa} >= %{gnome_bluetooth_version}
%endif
Requires:       gnome-desktop3%{?_isa} >= %{gnome_desktop_version}
%if 0%{?rhel} != 7
# Disabled on RHEL 7 to allow logging into KDE session by default
Recommends:     gnome-session-xsession
%endif
Requires:       gcr%{?_isa}
Requires:       gobject-introspection%{?_isa} >= %{gobject_introspection_version}
Requires:       gjs%{?_isa} >= %{gjs_version}
Requires:       gtk3%{?_isa} >= %{gtk3_version}
Requires:       gtk4%{?_isa} >= %{gtk4_version}
Requires:       libadwaita%{_isa} >= %{adwaita_version}
Requires:       libnma-gtk4%{?_isa}
# needed for loading SVG's via gdk-pixbuf
Requires:       librsvg2%{?_isa}
Requires:       mutter%{?_isa} >= %{mutter_version}
Requires:       upower%{?_isa}
Requires:       polkit%{?_isa} >= %{polkit_version}
Requires:       gnome-desktop4%{?_isa} >= %{gnome_desktop_version}
Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}
Requires:       gnome-settings-daemon%{?_isa} >= %{gnome_settings_daemon_version}
Requires:       gstreamer1%{?_isa} >= %{gstreamer_version}
# needed for screen recorder
Requires:       gstreamer1-plugins-good%{?_isa}
Requires:       pipewire-gstreamer%{?_isa}
Requires:       xdg-user-dirs-gtk
# needed for schemas
Requires:       at-spi2-atk%{?_isa}
# needed for on-screen keyboard
Requires:       ibus%{?_isa} >= %{ibus_version}
# needed for "show keyboard layout"
Requires:       libgnomekbd
# needed for the user menu
Requires:       accountsservice-libs%{?_isa}
Requires:       gdm-libs%{?_isa}
# needed for settings items in menus
Requires:       gnome-control-center
# needed by some utilities
Requires:       python3%{_isa}
# needed for the dual-GPU launch menu
Requires:       switcheroo-control
# needed for clocks/weather integration
Requires:       geoclue2-libs%{?_isa}
Requires:       libgweather4%{?_isa}
# needed for thunderbolt support
Requires:       bolt%{?_isa}
# Needed for launching flatpak apps etc
# 1.8.0 is needed for source type support in the screencast portal.
Requires:       xdg-desktop-portal-gtk >= 1.8.0
Requires:       xdg-desktop-portal-gnome
# needed by the welcome dialog
Recommends:     gnome-tour

Provides:       desktop-notification-daemon = %{version}-%{release}
Provides:       PolicyKit-authentication-agent = %{version}-%{release}
Provides:       bundled(gvc)
Provides:       bundled(libcroco) = 0.6.13

%if 0%{?rhel}
# In Fedora, fedora-obsolete-packages obsoletes caribou
Obsoletes:      caribou < 0.4.21-10
Obsoletes:      caribou-antler < 0.4.21-10
Obsoletes:      caribou-devel < 0.4.21-10
Obsoletes:      caribou-gtk2-module < 0.4.21-10
Obsoletes:      caribou-gtk3-module < 0.4.21-10
Obsoletes:      python-caribou < 0.4.21-10
Obsoletes:      python2-caribou < 0.4.21-10
Obsoletes:      python3-caribou < 0.4.21-10
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1740897
Conflicts:      gnome-shell-extension-background-logo < 3.34.0

%description
GNOME Shell provides core user interface functions for the GNOME 3 desktop,
like switching to windows and launching applications. GNOME Shell takes
advantage of the capabilities of modern graphics hardware and introduces
innovative user interface concepts to provide a visually attractive and
easy to use experience.

%prep
%autosetup -S git -n %{name}-%{tarball_version}

%build
%meson -Dextensions_app=false
%meson_build

%install
%meson_install

# Create empty directories where other packages can drop extensions
mkdir -p %{buildroot}%{_datadir}/gnome-shell/extensions
mkdir -p %{buildroot}%{_datadir}/gnome-shell/search-providers

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Shell.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Shell.Extensions.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Shell.PortalHelper.desktop

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/gnome-shell
%{_bindir}/gnome-extensions
%{_bindir}/gnome-shell-extension-prefs
%{_bindir}/gnome-shell-extension-tool
%{_bindir}/gnome-shell-perf-tool
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/glib-2.0/schemas/00_org.gnome.shell.gschema.override
%{_datadir}/applications/org.gnome.Shell.Extensions.desktop
%{_datadir}/applications/org.gnome.Shell.desktop
%{_datadir}/applications/org.gnome.Shell.PortalHelper.desktop
%{_datadir}/bash-completion/completions/gnome-extensions
%{_datadir}/gnome-control-center/keybindings/50-gnome-shell-launchers.xml
%{_datadir}/gnome-control-center/keybindings/50-gnome-shell-screenshots.xml
%{_datadir}/gnome-control-center/keybindings/50-gnome-shell-system.xml
%{_datadir}/gnome-shell/
%{_datadir}/dbus-1/services/org.gnome.ScreenSaver.service
%{_datadir}/dbus-1/services/org.gnome.Shell.CalendarServer.service
%{_datadir}/dbus-1/services/org.gnome.Shell.Extensions.service
%{_datadir}/dbus-1/services/org.gnome.Shell.HotplugSniffer.service
%{_datadir}/dbus-1/services/org.gnome.Shell.Notifications.service
%{_datadir}/dbus-1/services/org.gnome.Shell.PortalHelper.service
%{_datadir}/dbus-1/services/org.gnome.Shell.Screencast.service
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.Extensions.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.Introspect.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.PadOsd.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.Screencast.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.Screenshot.xml
%{_datadir}/dbus-1/interfaces/org.gnome.ShellSearchProvider.xml
%{_datadir}/dbus-1/interfaces/org.gnome.ShellSearchProvider2.xml
%{_datadir}/icons/hicolor/scalable/apps/org.gnome.Shell.Extensions.svg
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.Shell.Extensions-symbolic.svg
%{_userunitdir}/org.gnome.Shell-disable-extensions.service
%{_userunitdir}/org.gnome.Shell.target
%{_userunitdir}/org.gnome.Shell@wayland.service
%{_userunitdir}/org.gnome.Shell@x11.service
# Co own directory instead of pulling in xdg-desktop-portal - we
# are providing a backend to the portal, not depending on it
%dir %{_datadir}/xdg-desktop-portal/portals/
%{_datadir}/xdg-desktop-portal/portals/gnome-shell.portal
%{_libdir}/gnome-shell/
%{_libexecdir}/gnome-shell-calendar-server
%{_libexecdir}/gnome-shell-perf-helper
%{_libexecdir}/gnome-shell-hotplug-sniffer
%{_libexecdir}/gnome-shell-portal-helper
%{_mandir}/man1/gnome-extensions.1*
%{_mandir}/man1/gnome-shell.1*

%changelog
* Sat Mai 2023 Florian Müllner <fmuellner@gnome.org> - 44.1-faster
- Use Clang Toolchain
- Use LTO for default

* Tue Apr 25 2023 Florian Müllner <fmuellner@gnome.org> - 44.1-1
- Update to 44.1

44.1
====
* Add section title in background apps menu [Florian; !2681]
* Fix visibility of xembed icons [Marco; !2684]
* Fix placeholder alignment in bluetooth menu [Sebastian; !2687]
* Fix recording screenshots in recent items [Carlos, Adam; !2692, !2725]
* Fix reloading extensions on version-validation changes [Florian; !2694]
* Fix force-enabling animations at runtime [Florian; !2698]
* Fix stuck session after logout dialog timeout [Florian; !2696]
* Fix window screenshots with pointer [Ivan; !2710, !2702]
* Only show network subtitles if they don't match the title [Georges; !2682]
* Fix constructing QuickMenuToggles with icon-name [Florian; !2726]
* Fix accessible names in VPN menu [Lukáš; !2720]
* Don't fail extracting extensions without schemas [Andy; !2727]
* Fixes and improvements to the light theme variant [Sam; !2515]
* Improve accessible name of wireless menu items [Lukáš; !2724]
* Use consistent naming for "Power Mode" toggle [Automeris; !2697]
* Fix support for transparent colors in symbolic SVGs [Florian; !2731]
* Fix notifications getting stuck indefinitely [msizanoen1; !2736]
* Fix keynav of menu-less buttons [Florian; !2734]
* Fix corner cases when matching apps on StartupWmClass [Marco; !2721]
* Fix occasional misalignment of search results [Sebastian; !2744]
* Fix regression in content-type sniffing on autorun [Balló; !2745]
* Fix building API documentation [Bobby; !2749]
* Fixed crash [Jonas Å.; !2722]
* Plugged leak [Sebastian; !2737]
* Misc. bug fixes and cleanups [Florian, Will, Daniel, Marco, Sebastian,
  Jordan, Jonas D.; !2679, !2689, !2693, !2639, !2661, !2685, !2709, !2699,
  !2711, !2723, !2728, !2730, !2739, !2738, !2740, !2712, !2695, !2193]

Contributors:
  Jonas Ådahl, Jonas Dreßler, Carlos Garnacho, Balló György, Sam Hewitt,
  Andy Holmes, Sebastian Keller, Ivan Molodetskikh, msizanoen1, Florian Müllner,
  Automeris naranja, Georges Basile Stavracas Neto, Jordan Petridis, Bobby Rong,
  Will Thompson, Marco Trevisan (Treviño), Lukáš Tyrychtr, Daniel van Vugt,
  Adam Williamson

Translators:
  Fran Dieguez [gl], Balázs Úr [hu], Andika Triwidada [id], Anders Jonsson [sv],
  Martin [sl], Danial Behzadi [fa], Bruce Cowan [en_GB], Rūdolfs Mazurs [lv],
  Asier Sarasua Garmendia [eu], Nathan Follens [nl], Sabri Ünal [tr],
  Boyuan Yang [zh_CN], Guillaume Bernard [fr], Alexander Shopov [bg],
  Aleksandr Melman [ru], MohammadSaleh Kamyab [fa], Yuri Chornoivan [uk],
  Hugo Carvalho [pt], Fabio Tomat [fur], Kukuh Syafaat [id], Piotr Drąg [pl],
  Марко Костић [sr], Aurimas Černius [lt], Yaron Shahrabani [he],
  Philipp Kiemle [de]


