Name:           btrfs-snapshot-manager
Version:        1.0
Release:        1%{?dist}
Summary:        A GTK4 desktop application to manage Btrfs snapshots visually

License:        GPL-3.0
URL:            https://github.com/lagunamanuel/btrfs-snapshot-manager
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       btrfs-progs
Requires:       polkit

%description
Btrfs Snapshot Manager is a GTK4 desktop application built with Python
and libadwaita for native GNOME integration. It allows users to list,
create and delete Btrfs snapshots visually without using the terminal.

%prep
%autosetup

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/%{name}
mkdir -p %{buildroot}/usr/share/applications

install -m 755 main.py %{buildroot}/usr/share/%{name}/main.py
install -m 644 btrfs.py %{buildroot}/usr/share/%{name}/btrfs.py
install -m 644 window.py %{buildroot}/usr/share/%{name}/window.py

# Launcher script
cat > %{buildroot}/usr/bin/%{name} << 'LAUNCHER'
#!/bin/bash
cd /usr/share/%{name}
exec python3 main.py "$@"
LAUNCHER
chmod 755 %{buildroot}/usr/bin/%{name}

# Desktop entry
cat > %{buildroot}/usr/share/applications/%{name}.desktop << 'DESKTOP'
[Desktop Entry]
Name=Btrfs Snapshot Manager
Comment=Manage Btrfs snapshots visually
Exec=btrfs-snapshot-manager
Icon=drive-harddisk
Terminal=false
Type=Application
Categories=System;
DESKTOP

%files
/usr/bin/%{name}
/usr/share/%{name}/main.py
/usr/share/%{name}/btrfs.py
/usr/share/%{name}/window.py
/usr/share/applications/%{name}.desktop

%changelog
* Thu Jun 18 2026 Manuel Laguna <manuel@example.com> - 1.0-1
- Initial release
